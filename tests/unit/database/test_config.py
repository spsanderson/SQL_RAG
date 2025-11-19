"""
Test Database Configuration
"""
import pytest
from pydantic import ValidationError
from src.database.models import DatabaseConfig

def test_database_config_valid():
    """
    Test that a valid configuration is accepted.
    """
    config = DatabaseConfig(
        host="localhost",
        database="test_db",
        username="user",
        password="password"
    )
    assert config.host == "localhost"
    assert config.port == 1433
    assert config.driver == "ODBC Driver 17 for SQL Server"

def test_database_config_missing_required():
    """
    Test that missing required fields raises ValidationError.
    """
    with pytest.raises(ValidationError):
        DatabaseConfig(
            host="localhost",
            username="user"
            # Missing database and password
        )
