import pytest
from fastapi.testclient import TestClient
from src.api.main import app


def test_health_endpoint():
    """Test the health endpoint returns 200 status code."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_health_endpoint_root():
    """Test the root endpoint returns 200 status code."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}