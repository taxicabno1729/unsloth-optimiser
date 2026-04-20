"""Integration tests for task API endpoints."""
from datetime import datetime, timezone
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.api.main import app
from src.api.database import get_db
from src.api.models.task import TaskStatusEnum, OptimizationMethodEnum


def get_mock_db_session(task_name="test_quantization"):
    """Create a mock database session."""
    mock_db = MagicMock()
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.task_id = "test-task-123"
    mock_task.name = task_name
    mock_task.optimization_method = OptimizationMethodEnum.QUANTIZATION
    mock_task.status = TaskStatusEnum.PENDING
    mock_task.model_name = "test_model"
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


def test_complete_workflow():
    """Test end-to-end task creation and processing"""
    # Override the database dependency
    app.dependency_overrides[get_db] = lambda: get_mock_db_session()
    
    # Mock the orchestrator and set in app state
    mock_orchestrator = MagicMock()
    mock_orchestrator.schedule_task.return_value = "celery-task-456"
    app.state.orchestrator = mock_orchestrator
    
    client = TestClient(app)
    
    # Step 1: Create task
    response = client.post("/api/v1/tasks/", json={
        "name": "test_quantization",
        "optimization_method": "quantization",
        "model_name": "test_model"
    })
    assert response.status_code == 201
    task_data = response.json()
    assert "task_id" in task_data
    assert "celery_task_id" in task_data  # Should have celery task ID
    
    # Step 2: Get task status
    task_id = task_data["task_id"]
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "pending"
    
    # Clean up
    app.dependency_overrides.pop(get_db, None)


def test_task_creation_with_all_methods():
    """Test task creation for all optimization methods"""
    # Override the dependency
    app.dependency_overrides[get_db] = lambda: get_mock_db_session()
    
    # Mock the orchestrator and set in app state
    mock_orchestrator = MagicMock()
    mock_orchestrator.schedule_task.return_value = "celery-task-456"
    app.state.orchestrator = mock_orchestrator
    
    client = TestClient(app)
    methods = ["quantization", "lora", "awq", "gptq"]
    
    for method in methods:
        response = client.post("/api/v1/tasks/", json={
            "name": f"test_{method}",
            "optimization_method": method,
            "model_name": "test_model"
        })
        assert response.status_code == 201, f"Failed for method: {method}"
        data = response.json()
        assert data["optimization_method"] == method
    
    # Clean up
    app.dependency_overrides.pop(get_db, None)
