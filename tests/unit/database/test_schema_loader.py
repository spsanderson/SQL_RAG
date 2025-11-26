"""
Unit tests for SchemaLoader.
"""
import pytest
from unittest.mock import MagicMock
from src.database.schema_loader import SchemaLoader
from src.database.connection_pool import ConnectionPool

def test_load_schema():
    mock_pool = MagicMock(spec=ConnectionPool)
    mock_adapter = MagicMock()
    mock_pool.get_adapter.return_value = mock_adapter
    mock_adapter.get_schema.return_value = ["schema"]
    
    loader = SchemaLoader(mock_pool)
    schema = loader.load_schema()
    
    assert schema == ["schema"]
    mock_pool.get_adapter.assert_called_once()
    mock_adapter.get_schema.assert_called_once()
