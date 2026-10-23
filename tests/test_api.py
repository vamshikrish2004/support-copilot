from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_empty_message_rejected():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 422


def test_too_long_message_rejected():
    response = client.post("/chat", json={"message": "a" * 1001})
    assert response.status_code == 422


def test_missing_message_rejected():
    response = client.post("/chat", json={})
    assert response.status_code == 422