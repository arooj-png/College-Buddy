# backend/test_app.py - simple pytest for the API (uses TestClient)
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_query_endpoint_status_and_schema():
    res = client.post("/api/query", json={"question": "Hello? This is a test.", "mood": "casual"})
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
