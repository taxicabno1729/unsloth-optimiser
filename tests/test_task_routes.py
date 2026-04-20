"""Tests for task management endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.main import app
from src.api.database import get_db
from src.api.models.base import Base


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def setup_db():
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_task_endpoint(setup_db):
    client = TestClient(app)
    response = client.post("/api/v1/tasks/", json={
        "name": "test_task",
        "optimization_method": "quantization",
        "model_name": "test_model"
    })
    assert response.status_code == 201
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "pending"


def test_get_task_status(setup_db):
    client = TestClient(app)
    # First create a task
    response = client.post("/api/v1/tasks/", json={
        "name": "test",
        "optimization_method": "quantization",
        "model_name": "test_model"
    })
    task_id = response.json()["task_id"]
    
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["task_id"] == task_id
