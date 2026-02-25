from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os

DATA_PATH = "data"
docs = []

for file in os.listdir(DATA_PATH):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(DATA_PATH, file))
        pages = loader.load()
        docs.extend(pages)

print(f"Loaded {len(docs)} pages")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

print(f"Created {len(chunks)} chunks")

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectordb = Chroma.from_documents(chunks, embeddings, persist_directory="./hr_vectordb")

vectordb.persist()
print("✅ HR knowledge base ready!")
