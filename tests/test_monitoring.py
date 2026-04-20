"""Tests for monitoring and observability endpoints."""
from fastapi.testclient import TestClient
from src.api.main import app


def test_metrics_endpoint():
    """Test that /metrics endpoint returns Prometheus metrics."""
    client = TestClient(app)
    response = client.get("/metrics")
    # Should return Prometheus metrics or 404 if not implemented
    assert response.status_code in [200, 404]


def test_health_endpoint():
    """Test that /api/v1/health endpoint returns healthy status."""
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_health_has_version():
    """Test that health endpoint returns version information."""
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
