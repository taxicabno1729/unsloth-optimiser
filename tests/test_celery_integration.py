"""Tests for Celery integration."""
import pytest


def test_celery_app_initialization():
    """Test that Celery app is properly initialized."""
    from src.api.tasks.celery import celery_app
    assert celery_app.main == "unsloth-optimiser-worker"
    assert callable(celery_app.send_task)


def test_optimization_task_signature():
    """Test that optimization task signature can be created."""
    from src.api.tasks.celery import celery_app
    from src.api.schemas.task import OptimizationMethod

    signature = celery_app.signature(
        "optimization_worker.process_task",
        args=[{"name": "test", "method": "quantization"}]
    )
    assert signature.task == "optimization_worker.process_task"


def test_worker_task_names():
    """Test that all worker tasks are registered with correct names."""
    from src.api.workers.optimization_worker import (
        process_quantization,
        process_lora,
        process_awq,
        process_gptq,
        optimization_worker,
    )

    assert process_quantization.name == "optimization_worker.process_quantization"
    assert process_lora.name == "optimization_worker.process_lora"
    assert process_awq.name == "optimization_worker.process_awq"
    assert process_gptq.name == "optimization_worker.process_gptq"
    assert optimization_worker.name == "optimization_worker.process_task"


def test_process_quantization_task():
    """Test quantization task execution."""
    from src.api.workers.optimization_worker import process_quantization

    config = {"model_name": "test-model", "bits": 4}
    result = process_quantization(config)

    assert result["status"] == "success"
    assert result["method"] == "quantization"
    assert result["details"] == config


def test_process_lora_task():
    """Test LoRA task execution."""
    from src.api.workers.optimization_worker import process_lora

    config = {"model_name": "test-model", "rank": 8}
    result = process_lora(config)

    assert result["status"] == "success"
    assert result["method"] == "lora"
    assert result["details"] == config


def test_process_awq_task():
    """Test AWQ task execution."""
    from src.api.workers.optimization_worker import process_awq

    config = {"model_name": "test-model", "bits": 4}
    result = process_awq(config)

    assert result["status"] == "success"
    assert result["method"] == "awq"
    assert result["details"] == config


def test_process_gptq_task():
    """Test GPTQ task execution."""
    from src.api.workers.optimization_worker import process_gptq

    config = {"model_name": "test-model", "bits": 4}
    result = process_gptq(config)

    assert result["status"] == "success"
    assert result["method"] == "gptq"
    assert result["details"] == config


def test_optimization_worker_routing_quantization():
    """Test that optimization worker routes to quantization."""
    from src.api.workers.optimization_worker import optimization_worker
    from src.api.schemas.task import OptimizationMethod

    config = {
        "optimization_method": OptimizationMethod.QUANTIZATION.value,
        "model_name": "test"
    }
    result = optimization_worker(config)

    assert result["status"] == "success"
    assert result["method"] == "quantization"


def test_optimization_worker_routing_lora():
    """Test that optimization worker routes to LoRA."""
    from src.api.workers.optimization_worker import optimization_worker
    from src.api.schemas.task import OptimizationMethod

    config = {
        "optimization_method": OptimizationMethod.LORA.value,
        "model_name": "test"
    }
    result = optimization_worker(config)

    assert result["status"] == "success"
    assert result["method"] == "lora"


def test_optimization_worker_routing_awq():
    """Test that optimization worker routes to AWQ."""
    from src.api.workers.optimization_worker import optimization_worker
    from src.api.schemas.task import OptimizationMethod

    config = {
        "optimization_method": OptimizationMethod.AWQ.value,
        "model_name": "test"
    }
    result = optimization_worker(config)

    assert result["status"] == "success"
    assert result["method"] == "awq"


def test_optimization_worker_routing_gptq():
    """Test that optimization worker routes to GPTQ."""
    from src.api.workers.optimization_worker import optimization_worker
    from src.api.schemas.task import OptimizationMethod

    config = {
        "optimization_method": OptimizationMethod.GPTQ.value,
        "model_name": "test"
    }
    result = optimization_worker(config)

    assert result["status"] == "success"
    assert result["method"] == "gptq"


def test_optimization_worker_invalid_method():
    """Test that optimization worker raises error for invalid method."""
    from src.api.workers.optimization_worker import optimization_worker

    config = {
        "optimization_method": "invalid_method",
        "model_name": "test"
    }

    with pytest.raises(ValueError) as exc_info:
        optimization_worker(config)

    assert "Unknown optimization method" in str(exc_info.value)
    assert "invalid_method" in str(exc_info.value)
