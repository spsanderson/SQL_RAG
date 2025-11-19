"""
Test Connection Pool
"""
import pytest
from unittest.mock import MagicMock, patch
from src.database.connection_pool import ConnectionPool
from src.database.models import DatabaseConfig

@pytest.fixture
def db_config():
    return DatabaseConfig(
        host="localhost",
        database="test_db",
        username="user",
        password="password"
    )

def test_connection_pool_initialization(db_config):
    """
    Test that the connection pool initializes correctly.
    """
    pool = ConnectionPool(db_config)
    assert pool.config == db_config
    assert pool._engine is None

@patch('src.database.adapters.sqlserver_adapter.create_engine')
def test_get_engine_creates_engine(mock_create_engine, db_config):
    """
    Test that get_engine creates an engine if one doesn't exist.
    """
    pool = ConnectionPool(db_config)
    engine = pool.get_engine()
    
    assert mock_create_engine.called
    assert engine is not None
    assert pool._engine is not None

@patch('src.database.adapters.sqlserver_adapter.create_engine')
def test_get_engine_returns_existing(mock_create_engine, db_config):
    """
    Test that get_engine returns the existing engine if called twice.
    """
    pool = ConnectionPool(db_config)
    engine1 = pool.get_engine()
    engine2 = pool.get_engine()
    
    assert mock_create_engine.call_count == 1
    assert engine1 is engine2
