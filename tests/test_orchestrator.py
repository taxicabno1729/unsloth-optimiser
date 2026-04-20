"""Tests for task orchestration and management service."""
import pytest
from unittest.mock import patch, MagicMock


def test_task_orchestration():
    from src.api.tasks.orchestrator import TaskOrchestrator

    orchestrator = TaskOrchestrator()
    assert orchestrator is not None
    assert hasattr(orchestrator, 'schedule_task')
    assert hasattr(orchestrator, 'validate_config')


def test_task_manager_initialization():
    from src.api.tasks.manager import TaskManager

    manager = TaskManager()
    assert manager is not None


def test_orchestrator_worker_mapping():
    from src.api.tasks.orchestrator import TaskOrchestrator
    from src.api.schemas.task import OptimizationMethod

    orchestrator = TaskOrchestrator()
    assert OptimizationMethod.QUANTIZATION in orchestrator.worker_mapping
    assert OptimizationMethod.LORA in orchestrator.worker_mapping
    assert OptimizationMethod.AWQ in orchestrator.worker_mapping
    assert OptimizationMethod.GPTQ in orchestrator.worker_mapping


def test_orchestrator_validate_config():
    from src.api.tasks.orchestrator import TaskOrchestrator
    from src.api.schemas.task import TaskCreate, OptimizationMethod

    orchestrator = TaskOrchestrator()

    # Valid config
    valid_config = TaskCreate(
        name="test_task",
        optimization_method=OptimizationMethod.QUANTIZATION,
        model_name="meta-llama/Llama-2-7b",
        parameters={},
        user_id="user123"
    )
    assert orchestrator.validate_config(valid_config) is True

    # Test validation with config object that has empty name (simulated by direct manipulation)
    # Pydantic won't allow creating this directly, so we test via mock
    class MockConfig:
        name = ""
        model_name = "meta-llama/Llama-2-7b"
        optimization_method = OptimizationMethod.QUANTIZATION

    assert orchestrator.validate_config(MockConfig()) is False

    # Invalid config - empty model_name
    class MockConfig2:
        name = "test_task"
        model_name = ""
        optimization_method = OptimizationMethod.QUANTIZATION

    assert orchestrator.validate_config(MockConfig2()) is False


def test_orchestrator_validate_config_invalid_method():
    from src.api.tasks.orchestrator import TaskOrchestrator
    from src.api.schemas.task import TaskCreate, OptimizationMethod

    orchestrator = TaskOrchestrator()

    # Valid config with all methods
    for method in OptimizationMethod:
        config = TaskCreate(
            name=f"test_{method.value}",
            optimization_method=method,
            model_name="meta-llama/Llama-2-7b",
            parameters={},
            user_id="user123"
        )
        assert orchestrator.validate_config(config) is True


def test_orchestrator_schedule_task_validates_config():
    from src.api.tasks.orchestrator import TaskOrchestrator
    from src.api.schemas.task import OptimizationMethod

    orchestrator = TaskOrchestrator()

    # Create a mock invalid config (simulating one that would fail validation)
    class MockInvalidConfig:
        name = ""  # Empty name should fail validation
        model_name = "meta-llama/Llama-2-7b"
        optimization_method = OptimizationMethod.QUANTIZATION

    # Invalid config should raise ValueError
    with pytest.raises(ValueError, match="Invalid task configuration"):
        orchestrator.schedule_task(MockInvalidConfig(), "task-123")


@patch('src.api.tasks.orchestrator.app')
def test_orchestrator_schedule_task_success(mock_app):
    from src.api.tasks.orchestrator import TaskOrchestrator
    from src.api.schemas.task import TaskCreate, OptimizationMethod

    # Mock the Celery result
    mock_result = MagicMock()
    mock_result.id = "celery-task-id-123"
    mock_app.send_task.return_value = mock_result

    orchestrator = TaskOrchestrator()
    config = TaskCreate(
        name="test_task",
        optimization_method=OptimizationMethod.QUANTIZATION,
        model_name="meta-llama/Llama-2-7b",
        parameters={"bits": 4},
        user_id="user123"
    )

    result = orchestrator.schedule_task(config, "task-123")

    assert result == "celery-task-id-123"
    mock_app.send_task.assert_called_once()
    call_args = mock_app.send_task.call_args
    assert call_args[0][0] == "optimization_worker.process_quantization"
    assert call_args[1]["kwargs"]["config"]["name"] == "test_task"


@patch('src.api.tasks.orchestrator.app')
def test_orchestrator_schedule_task_worker_mapping(mock_app):
    from src.api.tasks.orchestrator import TaskOrchestrator
    from src.api.schemas.task import TaskCreate, OptimizationMethod

    mock_result = MagicMock()
    mock_result.id = "celery-task-id"
    mock_app.send_task.return_value = mock_result

    orchestrator = TaskOrchestrator()

    expected_workers = {
        OptimizationMethod.QUANTIZATION: "optimization_worker.process_quantization",
        OptimizationMethod.LORA: "optimization_worker.process_lora",
        OptimizationMethod.AWQ: "optimization_worker.process_awq",
        OptimizationMethod.GPTQ: "optimization_worker.process_gptq",
    }

    for method, expected_worker in expected_workers.items():
        config = TaskCreate(
            name=f"test_{method.value}",
            optimization_method=method,
            model_name="meta-llama/Llama-2-7b",
            parameters={},
            user_id="user123"
        )

        orchestrator.schedule_task(config, f"task-{method.value}")

        # Check that the correct worker was called
        call_args = mock_app.send_task.call_args
        assert call_args[0][0] == expected_worker


def test_orchestrator_schedule_task_unknown_method():
    from src.api.tasks.orchestrator import TaskOrchestrator
    from src.api.schemas.task import OptimizationMethod

    orchestrator = TaskOrchestrator()

    # Create a valid config with a method that is in mapping
    class MockValidConfig:
        name = "test_task"
        model_name = "meta-llama/Llama-2-7b"
        optimization_method = OptimizationMethod.QUANTIZATION

    # First verify it's valid with the mapping
    assert orchestrator.validate_config(MockValidConfig()) is True

    # Now temporarily clear the mapping to simulate no worker available
    # but keep the method in validate_config's check by using a different approach
    # We'll use a method that is NOT in the mapping
    class MockConfigWithUnknownMethod:
        name = "test_task"
        model_name = "meta-llama/Llama-2-7b"
        optimization_method = "unknown_method"  # Not in mapping

    with pytest.raises(ValueError, match="Invalid task configuration"):
        orchestrator.schedule_task(MockConfigWithUnknownMethod(), "task-123")


@patch('src.api.tasks.manager.get_db')
def test_task_manager_create_task_record(mock_get_db):
    from src.api.tasks.manager import TaskManager
    from src.api.schemas.task import TaskCreate, OptimizationMethod

    mock_db = MagicMock()
    mock_get_db.return_value = iter([mock_db])

    manager = TaskManager()
    task_data = TaskCreate(
        name="test_task",
        optimization_method=OptimizationMethod.QUANTIZATION,
        model_name="meta-llama/Llama-2-7b",
        parameters={"bits": 4},
        user_id="user123"
    )

    result = manager.create_task_record(task_data, "task-123", "celery-id-456")

    assert result is not None
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


@patch('src.api.tasks.manager.get_db')
def test_task_manager_update_task_status(mock_get_db):
    from src.api.tasks.manager import TaskManager
    from src.api.schemas.task import TaskStatus
    from src.api.models.task import Task as TaskModel

    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_task = MagicMock(spec=TaskModel)
    mock_query.filter.return_value.first.return_value = mock_task
    mock_db.query.return_value = mock_query
    mock_get_db.return_value = iter([mock_db])

    manager = TaskManager()
    result = manager.update_task_status("task-123", TaskStatus.RUNNING, {"progress": 50})

    assert result is not None
    assert mock_task.status.value == "running"
    mock_db.commit.assert_called_once()


@patch('src.api.tasks.manager.get_db')
def test_task_manager_get_task_by_id(mock_get_db):
    from src.api.tasks.manager import TaskManager
    from src.api.models.task import Task as TaskModel

    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_task = MagicMock(spec=TaskModel)
    mock_query.filter.return_value.first.return_value = mock_task
    mock_db.query.return_value = mock_query
    mock_get_db.return_value = iter([mock_db])

    manager = TaskManager()
    result = manager.get_task_by_id("task-123")

    assert result is not None


@patch('src.api.tasks.manager.get_db')
def test_task_manager_get_task_history(mock_get_db):
    from src.api.tasks.manager import TaskManager
    from src.api.models.task import Task as TaskModel

    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_tasks = [MagicMock(spec=TaskModel), MagicMock(spec=TaskModel)]
    mock_query.filter.return_value.order_by.return_value.limit.return_value.all.return_value = mock_tasks
    mock_db.query.return_value = mock_query
    mock_get_db.return_value = iter([mock_db])

    manager = TaskManager()
    result = manager.get_task_history(user_id="user123", limit=10)

    assert len(result) == 2


@patch('src.api.tasks.manager.get_db')
def test_task_manager_get_task_history_without_user(mock_get_db):
    from src.api.tasks.manager import TaskManager
    from src.api.models.task import Task as TaskModel

    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_tasks = [MagicMock(spec=TaskModel)]
    mock_query.order_by.return_value.limit.return_value.all.return_value = mock_tasks
    mock_db.query.return_value = mock_query
    mock_get_db.return_value = iter([mock_db])

    manager = TaskManager()
    result = manager.get_task_history(limit=5)

    # Should not call filter when user_id is None
    mock_query.filter.assert_not_called()
    assert len(result) == 1


@patch('src.api.tasks.manager.get_db')
def test_task_manager_update_task_status_not_found(mock_get_db):
    from src.api.tasks.manager import TaskManager
    from src.api.schemas.task import TaskStatus

    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db.query.return_value = mock_query
    mock_get_db.return_value = iter([mock_db])

    manager = TaskManager()
    result = manager.update_task_status("non-existent-task", TaskStatus.COMPLETED)

    assert result is None
