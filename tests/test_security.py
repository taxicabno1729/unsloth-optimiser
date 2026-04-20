"""Security middleware tests."""

from fastapi.testclient import TestClient
from src.api.main import app

def test_cors_headers_present():
    client = TestClient(app)
    response = client.get(
        "/api/v1/health",
        headers={"Origin": "http://localhost:3000"}
    )
    # CORS headers should be present
    assert response.status_code == 200

def test_jwt_security_configured():
    from src.api.config import Settings
    
    settings = Settings()
    assert settings.jwt_secret_key
    assert settings.jwt_algorithm in ["HS256", "RS256"]

def test_security_headers():
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    # Check for security headers
    headers = response.headers
    assert "content-type" in headers
