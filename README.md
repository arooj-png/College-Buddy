# 🎓 College Buddy — Your Campus Bestie 🤖

> *"Starting sophomore year and already building my own AI assistant...  
No big deal 😌"*

Welcome to **College Buddy** — a RAG-powered FAQ bot made for **NUST CEME**.  
It reads your college guidebooks, notes, and deadlines so you don’t have to.  
Ask it *“When’s the fee deadline?”* or *“What are hostel rules?”* and it answers instantly 💌

---

## 💡 What It Does

- 📖 Reads PDFs & text files of your college resources
- 💬 Gives natural-language answers (like a friendly senior 🧠)
- ⚡ Built with LangChain + Cohere + FastAPI
- 🎨 Has a cute frontend (because we love aesthetics 💅)

---

## 🧠 How It Works

PDFs/Notes → LangChain → Embeddings → ChromaDB
↓
Cohere LLM
↓
Answering your questions ✨

---

## 📂 Project Layout

college-buddy/
├── backend/
│ ├── main.py # FastAPI backend
│ ├── ingest.py # Makes vector DB from PDFs
│ ├── data/ # Put your PDFs here 📁
│ └── chroma_db/ # Auto-created DB
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
└── README.md

---

## ⚙️ Setup Guide

### 🧪 1. Clone this repo
```bash
git clone https://github.com/<your-username>/college-buddy.git
cd college-buddy
🌱 2. Create a virtual environment
bash
Copy code
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
📦 3. Install backend dependencies
bash
Copy code
cd backend
pip install -r requirements.txt
🔑 4. Add your Cohere API key
Make a .env file in backend/:

ini
Copy code
COHERE_API_KEY=your_api_key_here
📚 5. Add your guidebook PDF
Put your PDF (like NUST CEME Guidebook) into:

bash
Copy code
backend/data/
⚡ 6. Build the vector database
bash
Copy code
python ingest.py
🚀 7. Run the backend
bash
Copy code
uvicorn main:app --reload
💻 8. Open the frontend
Just open frontend/index.html in your browser.

📝 Notes
Backend runs on http://127.0.0.1:8000

Frontend talks to backend through /api/query

Make sure both run at the same time ✨

💖 About Me
🏫 Sophomore @ NUST CEME

☕ Currently surviving on coffee, code, and deadlines

💭 Dreaming about building cooler AI tools every day

📜 License
MIT License — because sharing is caring 💌
