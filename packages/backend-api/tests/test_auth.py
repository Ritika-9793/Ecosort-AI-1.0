import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "services" in data


def test_user_registration_validation():
    payload = {
        "full_name": "A", # invalid length
        "email": "invalid-email",
        "password": "short"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422
