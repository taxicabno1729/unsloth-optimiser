"""Worker implementations for optimization tasks."""

from src.api.tasks.celery import celery_app
from src.api.schemas.task import OptimizationMethod


@celery_app.task(name="optimization_worker.process_quantization")
def process_quantization(config: dict) -> dict:
    """Process 4-bit or 8-bit quantization.

    Args:
        config: Dictionary containing quantization configuration

    Returns:
        Dictionary with status, method and details
    """
    return {"status": "success", "method": "quantization", "details": config}


@celery_app.task(name="optimization_worker.process_lora")
def process_lora(config: dict) -> dict:
    """Process LoRA fine-tuning.

    Args:
        config: Dictionary containing LoRA configuration

    Returns:
        Dictionary with status, method and details
    """
    return {"status": "success", "method": "lora", "details": config}


@celery_app.task(name="optimization_worker.process_awq")
def process_awq(config: dict) -> dict:
    """Process Activation-aware Weight Quantization.

    Args:
        config: Dictionary containing AWQ configuration

    Returns:
        Dictionary with status, method and details
    """
    return {"status": "success", "method": "awq", "details": config}


@celery_app.task(name="optimization_worker.process_gptq")
def process_gptq(config: dict) -> dict:
    """Process GPTQ optimization.

    Args:
        config: Dictionary containing GPTQ configuration

    Returns:
        Dictionary with status, method and details
    """
    return {"status": "success", "method": "gptq", "details": config}


@celery_app.task(name="optimization_worker.process_task")
def optimization_worker(config: dict):
    """Worker for processing optimization tasks - routes to specific method.

    Args:
        config: Dictionary containing task configuration with optimization_method

    Returns:
        Result from the specific optimization method task

    Raises:
        ValueError: If optimization_method is unknown
    """
    method = config.get("optimization_method")

    if method == OptimizationMethod.QUANTIZATION.value:
        return process_quantization(config)
    elif method == OptimizationMethod.LORA.value:
        return process_lora(config)
    elif method == OptimizationMethod.AWQ.value:
        return process_awq(config)
    elif method == OptimizationMethod.GPTQ.value:
        return process_gptq(config)
    else:
        raise ValueError(f"Unknown optimization method: {method}")
