"""API configuration settings using Pydantic."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "unsloth-optimiser"
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql://user:pass@localhost/db"
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    api_v1_prefix: str = "/api/v1"
    testing: bool = False
