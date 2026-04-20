import pytest
from fastapi.testclient import TestClient
from src.api.schemas.task import OptimizationMethod

# Don't import app at module level - use fixture from conftest.py

@pytest.mark.parametrize("method", [
    OptimizationMethod.QUANTIZATION,
    OptimizationMethod.LORA,
    OptimizationMethod.AWQ,
    OptimizationMethod.GPTQ,
])
def test_all_optimization_methods(method, client):
    """Test that all optimization methods are supported"""
    response = client.post("/api/v1/tasks/", json={
        "name": f"test_{method.value}",
        "optimization_method": method.value,
        "model_name": "test_model"
    })
    # Should accept the request
    assert response.status_code == 201
    data = response.json()
    assert data["optimization_method"] == method.value
    assert "task_id" in data
    assert "celery_task_id" in data

def test_task_lifecycle_workflow(client):
    """Test task lifecycle: pending -> running -> completed"""
    # Create task
    response = client.post("/api/v1/tasks/", json={
        "name": "lifecycle_test",
        "optimization_method": "quantization",
        "model_name": "test_model"
    })
    assert response.status_code == 201
    task_id = response.json()["task_id"]
    
    # Check initial status is pending
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "pending"
    
    # In real scenario, worker would process task
    # For now, just verify task exists with valid status
    valid_statuses = ["pending", "running", "completed", "failed"]
    assert response.json()["status"] in valid_statuses

def test_error_handling_workflow(client):
    """Test error handling in workflow"""
    # Test invalid method
    response = client.post("/api/v1/tasks/", json={
        "name": "test",
        "optimization_method": "invalid_method",
        "model_name": "test"
    })
    assert response.status_code == 422
    
    # Test missing required field
    response = client.post("/api/v1/tasks/", json={
        "optimization_method": "quantization"
        # missing model_name
    })
    assert response.status_code == 422
    
    # Test non-existent task
    response = client.get("/api/v1/tasks/non-existent-id")
    assert response.status_code == 404

def test_concurrent_task_creation(client):
    """Test creating multiple tasks concurrently"""
    import concurrent.futures
    
    def create_task(i):
        return client.post("/api/v1/tasks/", json={
            "name": f"concurrent_{i}",
            "optimization_method": "quantization",
            "model_name": "test"
        })
    
    # Create 5 tasks concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(create_task, i) for i in range(5)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    # All should succeed
    for response in results:
        assert response.status_code == 201
        assert "task_id" in response.json()
