from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from prepare_embeddings import documents

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectordb = Chroma.from_documents(
    documents=documents, embedding=embeddings, persist_directory="./employee_vectordb"
)

vectordb.persist()
print("Employee data embedded successfully!")
