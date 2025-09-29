import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Rodel-Vita" in response.json()["message"]

def test_auth_protected():
    # Sin token -> 401
    response = client.get("/especialistas/")
    assert response.status_code == 401
