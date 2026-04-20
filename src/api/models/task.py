"""SQLAlchemy Task model for optimization jobs."""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from src.api.models.base import Base
import enum


class TaskStatusEnum(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class OptimizationMethodEnum(enum.Enum):
    QUANTIZATION = "quantization"
    LORA = "lora"
    AWQ = "awq"
    GPTQ = "gptq"


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    optimization_method = Column(SQLEnum(OptimizationMethodEnum))
    status = Column(SQLEnum(TaskStatusEnum), default=TaskStatusEnum.PENDING)
    model_name = Column(String)
    parameters = Column(JSON, default=dict)
    result = Column(JSON, nullable=True)
    user_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
