from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import sqlite3
import re

last_employee = None

# Load HR policy vector DB
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectordb = Chroma(persist_directory="./hr_vectordb", embedding_function=embeddings)

llm = OllamaLLM(model="llama3")


# ===================== SQL GENERATION =====================


def generate_sql(question):
    global last_employee

    schema = """
Table name: employees

Columns:
"Employee Name", "Employee Number", State, Zip, DOB, Age, Sex, MaritalDesc,
CitizenDesc, Hispanic/Latino, RaceDesc, "Date of Hire", "Date of Termination",
"Reason For Term", "Employment Status", Department, Position, "Pay Rate",
"Manager Name", "Employee Source", "Performance Score"
"""

    memory_context = ""
    if last_employee:
        memory_context = f"The last referenced employee is '{last_employee}'. Use this if the question refers to 'her', 'him', or omits the name."

    prompt = f"""
You are an expert SQL generator.

{memory_context}

Rules:
- Use only SELECT queries
- Table name is employees
- Employee names are stored as "Last, First"
- If user says "Mia Brown", search as:
  WHERE "Employee Name" LIKE '%Brown, Mia%'
- Wrap column names with spaces in double quotes
- If user asks "manager", use column "Manager Name"
- If user asks "pay" or "salary", use column "Pay Rate"
- If user asks "hire date", use column "Date of Hire"
- If user asks "termination", use column "Date of Termination"
- If user asks "performance", use column "Performance Score"
- Use single quotes for text values
- Do not include explanations

{schema}

User Question: {question}
SQL Query:
"""
    sql = llm.invoke(prompt).strip()
    return sql.replace("```sql", "").replace("```", "").strip()


# ===================== SQL CLEANUP =====================


def fix_column_names(sql):
    replacements = {
        "ManagerName": '"Manager Name"',
        "Manager_Name": '"Manager Name"',
        "PayRate": '"Pay Rate"',
        "Pay_Rate": '"Pay Rate"',
        "EmployeeName": '"Employee Name"',
        "DateOfHire": '"Date of Hire"',
        "DateOfTermination": '"Date of Termination"',
        "PerformanceScore": '"Performance Score"',
    }
    for wrong, correct in replacements.items():
        sql = sql.replace(wrong, correct)
    return sql


def normalize_name_in_query(sql):
    match = re.search(r"%([A-Za-z]+)\s([A-Za-z]+)%", sql)
    if match:
        first, last = match.groups()
        sql = sql.replace(f"%{first} {last}%", f"%{last}, {first}%")
    return sql


# ===================== DATABASE QUERY =====================


def query_database(question):
    global last_employee

    conn = sqlite3.connect("hr.db")
    cursor = conn.cursor()

    try:
        sql_query = normalize_name_in_query(fix_column_names(generate_sql(question)))
        print("Generated SQL:", sql_query)

        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()

        if not rows:
            return "No matching data found."

        # Single employee
        if len(rows) == 1:
            record = dict(zip(columns, rows[0]))
            last_employee = record.get("Employee Name")

            details = "\n".join([f"{col}: {record[col]}" for col in columns])
            return f"Here are the employee details:\n\n{details}"

        # Multiple results
        if len(rows) > 1:
            preview = rows[:5]
            return f"Found {len(rows)} records. Showing first 5:\n{preview}"

    except Exception as e:
        conn.close()
        return f"Sorry, I couldn't process that request. ({e})"


# ===================== RAG FOR HR POLICIES =====================


def rag_answer(question, chat_history):
    docs = vectordb.similarity_search(question, k=3)
    context = "\n\n".join([d.page_content for d in docs])

    history_text = "\n".join(
        [f"User: {h['user']}\nAssistant: {h['bot']}" for h in chat_history]
    )

    prompt = f"""
You are a helpful HR assistant.

Conversation so far:
{history_text}

Use ONLY the HR policy context below to answer.

HR Policy Context:
{context}

User Question: {question}
"""
    return llm.invoke(prompt)


# ===================== ROUTER =====================


def get_answer(question, chat_history):
    q = question.lower()

    # Route employee queries to SQL
    if (
        any(
            word in q
            for word in [
                "employee",
                "employees",
                "who",
                "list",
                "show",
                "salary",
                "pay",
                "performance",
                "manager",
                "department",
                "position",
                "details",
                "dob",
                "age",
                "state",
                "zip",
                "hire",
                "termination",
            ]
        )
        or "," in question
    ):
        return query_database(question)

    return rag_answer(question, chat_history)
