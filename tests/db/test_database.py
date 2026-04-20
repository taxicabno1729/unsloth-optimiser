"""Database operation tests following TDD approach."""
import pytest
from sqlalchemy.exc import OperationalError
from src.db.config.database import get_db_session, engine, Base
from src.db.models.optimization_config import OptimizationConfig
from src.db.models.task import Task
from src.db.models.result import Result


class TestDatabaseConnection:
    """Test database connection setup."""

    def test_database_engine_creation(self):
        """Test that database engine can be created."""
        assert engine is not None
        assert str(engine.url).startswith("postgresql")

    def test_database_connection_established(self):
        """Test that database connection can be established."""
        try:
            with engine.connect() as conn:
                result = conn.execute("SELECT 1")
                assert result.scalar() == 1
        except OperationalError:
            pytest.skip("Database not available for testing")

    def test_database_session_creation(self):
        """Test that database session can be created."""
        session = get_db_session()
        assert session is not None
        session.close()


class TestDatabaseModels:
    """Test database models for optimization configurations, tasks, and results."""

    def test_optimization_config_model_exists(self):
        """Test that OptimizationConfig model is properly defined."""
        assert hasattr(OptimizationConfig, '__tablename__')
        assert OptimizationConfig.__tablename__ == 'optimization_configs'

    def test_task_model_exists(self):
        """Test that Task model is properly defined."""
        assert hasattr(Task, '__tablename__')
        assert Task.__tablename__ == 'tasks'

    def test_result_model_exists(self):
        """Test that Result model is properly defined."""
        assert hasattr(Result, '__tablename__')
        assert Result.__tablename__ == 'results'

    def test_optimization_config_has_required_fields(self):
        """Test that OptimizationConfig has required fields."""
        assert hasattr(OptimizationConfig, 'id')
        assert hasattr(OptimizationConfig, 'name')
        assert hasattr(OptimizationConfig, 'optimization_method')
        assert hasattr(OptimizationConfig, 'parameters')
        assert hasattr(OptimizationConfig, 'status')

    def test_task_has_required_fields(self):
        """Test that Task has required fields."""
        assert hasattr(Task, 'id')
        assert hasattr(Task, 'config_id')
        assert hasattr(Task, 'status')
        assert hasattr(Task, 'progress')

    def test_result_has_required_fields(self):
        """Test that Result has required fields."""
        assert hasattr(Result, 'id')
        assert hasattr(Result, 'task_id')
        assert hasattr(Result, 'metrics')


class TestDatabaseSessionManagement:
    """Test proper session management and connection pooling."""

    def test_session_isolation(self):
        """Test that sessions are properly isolated."""
        session1 = get_db_session()
        session2 = get_db_session()
        assert session1 is not session2
        session1.close()
        session2.close()

    def test_session_cleanup_on_error(self):
        """Test that sessions are properly cleaned up on error."""
        session = get_db_session()
        # Simulate an error scenario
        session.rollback()
        session.close()

    def test_connection_pool_size(self):
        """Test that connection pooling is configured."""
        pool = engine.pool
        assert pool is not None
        # Check pool size is configured
        assert pool.size() >= 1

    def test_session_factory_returns_valid_session(self):
        """Test that session factory creates valid sessions."""
        from sqlalchemy.orm import Session
        # The get_db_session function creates new sessions via SessionLocal
        from src.db.config.database import SessionLocal
        session = SessionLocal()
        assert isinstance(session, Session)
        session.close()