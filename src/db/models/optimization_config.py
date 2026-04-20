"""Optimization configuration model."""
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from src.db.models.base import BaseModel


class OptimizationConfig(BaseModel):
    """Model for storing optimization configurations."""
    __tablename__ = "optimization_configs"

    name = Column(String(255), nullable=False, index=True)
    optimization_method = Column(Enum(
        "quantization", "lora", "awq", "gptq",
        name="optimization_method_enum"
    ), nullable=False)
    parameters = Column(JSONB, nullable=False)
    status = Column(Enum(
        "pending", "running", "completed", "failed",
        name="optimization_status_enum"
    ), default="pending")
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<OptimizationConfig(name='{self.name}', method='{self.optimization_method}')>"

    @property
    def tasks(self):
        """Lazy-loaded tasks relationship."""
        from src.db.models.task import Task
        return Task.query.filter_by(config_id=self.id).all()