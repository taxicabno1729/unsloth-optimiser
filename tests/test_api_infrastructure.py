"""Tests for core API infrastructure."""


def test_api_main_import():
    from src.api import main
    assert hasattr(main, 'app')
    assert main.app.title == "Unsloth Optimiser API"


def test_database_connection():
    from src.api.database import get_db
    assert callable(get_db)
