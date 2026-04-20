"""Task model for optimization tasks."""
from sqlalchemy import Column, Integer, String, Enum, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, backref
from src.db.models.base import BaseModel


class Task(BaseModel):
    """Model for tracking optimization tasks."""
    __tablename__ = "tasks"

    config_id = Column(Integer, ForeignKey("optimization_configs.id"), nullable=False)
    status = Column(Enum(
        "queued", "processing", "completed", "failed", "cancelled",
        name="task_status_enum"
    ), default="queued")
    progress = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    result_id = Column(Integer, ForeignKey("results.id"), nullable=True)

    # Relationships - use string names to avoid circular imports
    config = relationship("OptimizationConfig", back_populates="tasks")
    result = relationship("Result", back_populates="task")

    def __repr__(self):
        return f"<Task(id={self.id}, status='{self.status}')>"