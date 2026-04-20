"""Task Pydantic schemas for optimization jobs."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum


class OptimizationMethod(str, Enum):
    QUANTIZATION = "quantization"
    LORA = "lora"
    AWQ = "awq"
    GPTQ = "gptq"


class TaskCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    optimization_method: OptimizationMethod
    model_name: str = Field(..., min_length=1)
    parameters: dict = Field(default_factory=dict)
    user_id: Optional[str] = None


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    task_id: str
    name: str
    optimization_method: OptimizationMethod
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[dict] = None
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    celery_task_id: Optional[str] = None
