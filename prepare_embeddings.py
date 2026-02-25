import pandas as pd
from langchain_core.documents import Document

df = pd.read_csv("data/employees.csv")

documents = []

for _, row in df.iterrows():
    text = f"""
Employee Name: {row['Employee Name']}
Employee Number: {row['Employee Number']}
State: {row['State']}
Zip: {row['Zip']}
DOB: {row['DOB']}
Age: {row['Age']}
Sex: {row['Sex']}
Marital Status: {row['MaritalDesc']}
Citizenship: {row['CitizenDesc']}
Ethnicity: {row['Hispanic/Latino']}
Race: {row['RaceDesc']}
Hire Date: {row['Date of Hire']}
Termination Date: {row['Date of Termination']}
Employment Status: {row['Employment Status']}
Department: {row['Department']}
Position: {row['Position']}
Pay Rate: {row['Pay Rate']}
Manager: {row['Manager Name']}
Employee Source: {row['Employee Source']}
Performance Score: {row['Performance Score']}
"""
    documents.append(Document(page_content=text))

print(f"Prepared {len(documents)} employee documents.")
