# ingest.py - rebuild Chroma DB from backend/data/
import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

from langchain_cohere import CohereEmbeddings

load_dotenv()

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

def build_vectordb_from_folder(folder=DATA_DIR):
    docs = []
    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)
        if fname.lower().endswith('.txt'):
            docs.extend(TextLoader(path).load())
        elif fname.lower().endswith('.pdf'):
            docs.extend(PyPDFLoader(path).load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    # ✅ Use Cohere embeddings instead of Google
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        print("Error: COHERE_API_KEY environment variable not set.")
        print("Please set your Cohere API key in the .env file or as an environment variable.")
        print("Get your API key from: https://dashboard.cohere.ai/api-keys")
        return
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=cohere_api_key)

    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_DIR)
    vectordb.persist()
    print(f"Persisted Chroma DB to {CHROMA_DIR}")

if __name__ == '__main__':
    build_vectordb_from_folder()
