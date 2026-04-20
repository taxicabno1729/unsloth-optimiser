"""Test configuration and fixtures."""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test database URL before importing app
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["API_V1_PREFIX"] = "/api/v1"

from src.api.main import app
from src.api.database import Base, get_db
from src.api.tasks.orchestrator import TaskOrchestrator


# Create test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db dependency with test database."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create test database tables."""
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup after all tests
    Base.metadata.drop_all(bind=engine)
    # Remove test database file
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture
def client(monkeypatch):
    """Create test client with proper app state."""
    # Override database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Mock Celery send_task to avoid Redis connection
    class MockAsyncResult:
        def __init__(self, id):
            self.id = id
    
    def mock_send_task(task_name, kwargs=None, args=None, **options):
        # Return a mock result with a fake task id
        return MockAsyncResult(f"mock-celery-task-id-{task_name.replace('.', '-')}")
    
    from src.api.tasks import celery, orchestrator
    monkeypatch.setattr(celery.celery_app, "send_task", mock_send_task)
    
    # Initialize orchestrator on app state BEFORE creating TestClient
    app.state.orchestrator = TaskOrchestrator()
    
    # Create TestClient - don't use context manager to avoid triggering on_event
    test_client = TestClient(app)
    
    yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()
    if hasattr(app.state, "orchestrator"):
        delattr(app.state, "orchestrator")
