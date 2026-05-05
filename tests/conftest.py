import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from main import app
from config.db_connection import get_db_connection

@pytest.fixture
def mock_db():
    mock = MagicMock()
    # Mocking the context manager behavior for cursor
    mock_cursor = MagicMock()
    mock.cursor.return_value = mock_cursor
    return mock

@pytest.fixture
def client(mock_db):
    # Overriding dependency
    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db_connection] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
