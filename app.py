from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import uvicorn

from dotenv import load_dotenv
import asyncio

from langchain_cohere import CohereEmbeddings, ChatCohere

load_dotenv()
os.environ["COHERE_API_KEY"] = "H0DYJaoOVlec2NzceEUOLax1Re4SeTm82dCvV7kD"

app = FastAPI()

# Serve frontend static files
app.mount("/static", StaticFiles(directory="../frontend/dist"), name="static")

@app.get("/")
def read_index():
    return FileResponse("../frontend/dist/index.html")

# Use Cohere embeddings
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable not set. Please set your Cohere API key in the .env file or as an environment variable. Get your API key from: https://dashboard.cohere.ai/api-keys")
embeddings = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key=cohere_api_key)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")


class Query(BaseModel):
    question: str
    mood: str = "supportive"


def build_vectordb_from_folder(folder=DATA_DIR):
    docs = []
    if not os.path.exists(folder):
        print(f"No data folder found at {folder}")
        return None
    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)
        if fname.lower().endswith('.txt'):
            docs.extend(TextLoader(path).load())
        elif fname.lower().endswith('.pdf'):
            docs.extend(PyPDFLoader(path).load())
    if not docs:
        print("No documents loaded. Put .txt or .pdf files in backend/data/")
        return None
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_DIR)
    vectordb.persist()
    return vectordb


@app.on_event("startup")
async def startup_event():
    # build DB if missing
    if not os.path.exists(CHROMA_DIR) or not os.listdir(CHROMA_DIR):
        print("Building vector DB from files in backend/data/ ...")
        build_vectordb_from_folder()
    else:
        print("Chroma DB already exists. Loading...")


@app.post("/api/query")
async def query(q: Query):
    try:
        # Check if Chroma DB exists and has data
        if not os.path.exists(CHROMA_DIR) or not os.listdir(CHROMA_DIR):
            return {"answer": "Error: Vector database not found. Please run ingest.py first to build the database."}
        
        print(f"Processing query: {q.question}")
        vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
        retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        llm = ChatCohere(model="command-r", temperature=0.2, cohere_api_key=cohere_api_key)

        system_prompt = (
            "You are a supportive senior student helping juniors. Be friendly, casual, and encouraging. " 
            "Answer only using the retrieved documents. If not found, say you don't know and suggest where to check."
        )
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type='stuff')
        try:
            qa.combine_documents_chain.llm_chain.prompt.messages[0].content = system_prompt + f"\nTone: {q.mood}\n"
        except Exception:
            pass

        print("Running query with 30s timeout...")
        answer = await asyncio.wait_for(
            asyncio.to_thread(qa.run, q.question), 
            timeout=30.0
        )
        print("Query completed successfully")
        return {"answer": answer}
    
    except asyncio.TimeoutError:
        print("Query timed out after 30 seconds")
        return {"answer": "Sorry, the query timed out. Please try again with a simpler question."}
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        return {"answer": f"Error processing your question: {str(e)}"}


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
