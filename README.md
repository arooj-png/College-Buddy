Backend (FastAPI + LangChain + Chroma) - Testing enabled

Steps:
1. Put your campus .txt or .pdf files into backend/data/
2. Set your Google API key:
   export GOOGLE_API_KEY="your_key_here"   # Linux / macOS
   setx GOOGLE_API_KEY "your_key_here"     # Windows (PowerShell)
3. Create virtual env and install:
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
4. Build vector DB (optional, server startup will auto-build if DB missing):
   python ingest.py
5. Run server:
   uvicorn app:app --reload --port 8000
6. Run tests:
   pytest -q
