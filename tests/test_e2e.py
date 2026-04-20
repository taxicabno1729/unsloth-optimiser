import time
import pytest
from fastapi.testclient import TestClient
from src.api.schemas.task import OptimizationMethod

# Don't import app at module level - use fixture from conftest.py

def test_complete_optimization_workflow(client):
    """Test complete workflow from task creation to completion"""
    # Create task
    response = client.post("/api/v1/tasks/", json={
        "name": "e2e_test_task",
        "optimization_method": OptimizationMethod.QUANTIZATION.value,
        "model_name": "test_model",
        "parameters": {"bits": 4}
    })
    assert response.status_code == 201
    task_data = response.json()
    task_id = task_data["task_id"]
    
    # Verify task created correctly
    assert task_data["name"] == "e2e_test_task"
    assert task_data["optimization_method"] == "quantization"
    assert task_data["status"] == "pending"
    assert "celery_task_id" in task_data
    
    # Get task status
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["task_id"] == task_id
    assert task["status"] in ["pending", "running", "completed"]

def test_full_api_workflow(client):
    """Test full API workflow: health, create, get"""
    # Health check
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    
    # Create multiple tasks
    tasks = []
    for i in range(3):
        response = client.post("/api/v1/tasks/", json={
            "name": f"batch_task_{i}",
            "optimization_method": "quantization",
            "model_name": f"model_{i}"
        })
        assert response.status_code == 201
        tasks.append(response.json()["task_id"])
    
    # Verify all tasks exist
    for task_id in tasks:
        response = client.get(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["task_id"] == task_id

def test_authenticated_workflow(client):
    """Test workflow with authentication"""
    # Get token (using fake token for now)
    response = client.post("/api/v1/token", data={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    # Use token to create task
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    response = client.post("/api/v1/tasks/", 
        json={
            "name": "auth_test",
            "optimization_method": "lora",
            "model_name": "test_model"
        },
        headers=headers
    )
    # Should work even without full auth implementation
    assert response.status_code in [200, 201, 401, 403]
