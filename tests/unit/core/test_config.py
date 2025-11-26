"""
Unit tests for Config.
"""
import pytest
import os
from unittest.mock import patch, mock_open
from src.core.config import load_config, AppConfig, DatabaseConfig

def test_load_config_defaults():
    with patch.dict(os.environ, {}, clear=True):
        config = load_config()
        assert config.database.host == "localhost"
        assert config.database.type == "sqlserver"

def test_load_config_env_vars():
    env_vars = {
        "DB_HOST": "test-host",
        "DB_PORT": "1234",
        "DB_NAME": "test-db",
        "DB_USER": "test-user",
        "DB_PASSWORD": "test-password",
        "DB_TYPE": "sqlite"
    }
    with patch.dict(os.environ, env_vars, clear=True):
        config = load_config()
        assert config.database.host == "test-host"
        assert config.database.port == 1234
        assert config.database.type == "sqlite"

def test_load_config_file():
    yaml_content = """
    database:
      host: yaml-host
      port: 5678
    llm:
      model_name: yaml-model
    """
    with patch("builtins.open", mock_open(read_data=yaml_content)):
        with patch("os.path.exists", return_value=True):
            config = load_config("config.yaml")
            assert config.database.host == "yaml-host"
            assert config.database.port == 5678
            assert config.llm.model_name == "yaml-model"

def test_load_config_validation_error():
    # Test missing password for non-sqlite
    with patch.dict(os.environ, {"DB_TYPE": "sqlserver"}, clear=True):
        with pytest.raises(Exception): # ConfigurationError or ValueError
            load_config()
