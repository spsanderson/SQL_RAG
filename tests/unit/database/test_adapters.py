"""
Tests for Database Adapters
"""
import pytest
import os
from src.database.models import DatabaseConfig
from src.database.adapters.sqlite_adapter import SQLiteAdapter

@pytest.fixture
def sqlite_config():
    return DatabaseConfig(
        host="localhost",
        database=":memory:",
        username="user",
        password="password",
        type="sqlite"
    )

def test_sqlite_adapter_connection(sqlite_config):
    adapter = SQLiteAdapter(sqlite_config)
    assert adapter.validate_connection() is True

def test_sqlite_adapter_execute_query(sqlite_config):
    adapter = SQLiteAdapter(sqlite_config)
    # Create table
    adapter.execute_query("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    
    # Insert
    adapter.execute_query("INSERT INTO test (name) VALUES ('Alice')")
    
    # Select
    result = adapter.execute_query("SELECT * FROM test")
    assert result.row_count == 1
    assert result.rows[0]['name'] == 'Alice'
    


def test_sqlite_adapter_get_schema(sqlite_config):
    adapter = SQLiteAdapter(sqlite_config)
    adapter.execute_query("CREATE TABLE schema_test (id INTEGER, data TEXT)")
    
    schema = adapter.get_schema()
    table_names = [e.name for e in schema if e.type == 'table']
    assert "schema_test" in table_names

def test_sqlite_adapter_timeout(sqlite_config):
    adapter = SQLiteAdapter(sqlite_config)
    # SQLite doesn't support WAITFOR DELAY, but we can try a recursive query or large join
    # However, enforcing timeout in SQLite via SQLAlchemy execution_options is tricky as it depends on driver
    # For this test, we'll just verify the parameter is accepted and doesn't crash
    # In a real DB like SQL Server, we'd use WAITFOR DELAY
    try:
        adapter.execute_query("SELECT 1", timeout=1)
    except Exception as e:
        pytest.fail(f"Timeout parameter caused error: {e}")
    

