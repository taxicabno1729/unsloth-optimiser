"""End-to-end tests for task API."""
from datetime import datetime, timezone
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.api.main import app
from src.api.database import get_db
from src.api.models.task import TaskStatusEnum, OptimizationMethodEnum


def get_mock_db_session(task_name="e2e_test", task_id="test-task-123"):
    """Create a mock database session."""
    mock_db = MagicMock()
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.task_id = task_id
    mock_task.name = task_name
    mock_task.optimization_method = OptimizationMethodEnum.QUANTIZATION
    mock_task.status = TaskStatusEnum.PENDING
    mock_task.model_name = "meta-llama/Llama-2-7b"
    mock_task.parameters = {}
    mock_task.user_id = None
    mock_task.result = None
    mock_task.celery_task_id = "celery-task-456"
    mock_task.created_at = datetime.now(timezone.utc)
    mock_task.started_at = None
    mock_task.completed_at = None
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = mock_task
    return mock_db


def test_full_task_lifecycle():
    """Test complete task lifecycle from creation to status check"""
    # Set up mock orchestrator
    mock_orchestrator = MagicMock()
    mock_orchestrator.schedule_task.return_value = "celery-task-456"
    app.state.orchestrator = mock_orchestrator
    
    # Set up mock database dependency
    app.dependency_overrides[get_db] = lambda: get_mock_db_session()
    
    client = TestClient(app)
    
    # Create task
    response = client.post("/api/v1/tasks/", json={
        "name": "e2e_test",
        "optimization_method": "quantization",
        "model_name": "meta-llama/Llama-2-7b"
    })
    assert response.status_code == 201
    task_data = response.json()
    task_id = task_data["task_id"]
    
    # Verify task created with correct data
    assert task_data["name"] == "e2e_test"
    assert task_data["optimization_method"] == "quantization"
    assert task_data["status"] == "pending"
    assert "created_at" in task_data
    assert task_data["celery_task_id"] == "celery-task-456"
    
    # Update mock to return the correct task_id for GET request
    app.dependency_overrides[get_db] = lambda: get_mock_db_session(task_id=task_id)
    
    # Get task by ID
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["task_id"] == task_id
    
    # Clean up
    app.dependency_overrides.pop(get_db, None)


def test_invalid_task_method():
    """Test task creation with invalid method - FastAPI validation should catch this"""
    # Need to set up mock dependencies even for validation tests
    app.dependency_overrides[get_db] = lambda: get_mock_db_session()
    
    # Set up mock orchestrator (won't be called due to validation error)
    mock_orchestrator = MagicMock()
    app.state.orchestrator = mock_orchestrator
    
    client = TestClient(app)
    
    response = client.post("/api/v1/tasks/", json={
        "name": "test",
        "optimization_method": "invalid_method",
        "model_name": "test_model"
    })
    assert response.status_code == 422  # Validation error
    
    # Clean up
    app.dependency_overrides.pop(get_db, None)
