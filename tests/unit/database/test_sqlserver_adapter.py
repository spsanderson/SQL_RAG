"""
Unit tests for SQLServerAdapter.
"""
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.engine import URL
from src.database.adapters.sqlserver_adapter import SQLServerAdapter
from src.database.models import DatabaseConfig

@pytest.fixture
def db_config():
    return DatabaseConfig(
        host="localhost",
        database="testdb",
        username="sa",
        password="password",
        type="sqlserver",
        driver="ODBC Driver 17 for SQL Server"
    )

def test_build_connection_string(db_config):
    adapter = SQLServerAdapter(db_config)
    conn_url = adapter._build_connection_string()
    
    assert isinstance(conn_url, URL)
    assert conn_url.drivername == "mssql+pyodbc"
    assert conn_url.host == "localhost"
    assert conn_url.database == "testdb"
    assert conn_url.username == "sa"
    assert conn_url.password == "password"
    assert conn_url.query["driver"] == "ODBC Driver 17 for SQL Server"

@patch("src.database.adapters.sqlserver_adapter.create_engine")
def test_connect(mock_create_engine, db_config):
    adapter = SQLServerAdapter(db_config)
    engine = adapter.connect()
    
    mock_create_engine.assert_called_once()
    assert engine == mock_create_engine.return_value
    # Verify singleton
    assert adapter.connect() == engine
    mock_create_engine.assert_called_once()
