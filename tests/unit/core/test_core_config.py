"""
Unit tests for Config.
"""
import pytest
import os
from unittest.mock import patch, mock_open
from src.core.config import load_config, AppConfig, DatabaseConfig

def test_load_config_defaults():
    with patch.dict(os.environ, {"DB_PASSWORD": "default-password"}, clear=True):
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
      password: yaml-password
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

def test_load_multiple_configs():
    with patch.dict(os.environ, {"DB_PASSWORD": "env-password"}, clear=True):
        with patch("os.path.exists") as mock_exists:
            # Mock that all config files exist
            mock_exists.return_value = True
            
            mock_files = {
                os.path.join("config", "database.yaml"): """
                    database:
                      sql_server:
                        host: db-yaml-host
                """,
                os.path.join("config", "ollama.yaml"): """
                    ollama:
                      base_url: http://ollama-yaml:11434
                """,
                os.path.join("config", "rag.yaml"): """
                    rag:
                      vector_store:
                        collection_name: rag-yaml-collection
                """,
                os.path.join("config", "logging.yaml"): """
                    logging:
                      version: 1
                """,
                os.path.join("config", "security.yaml"): """
                    security:
                      auth:
                        enabled: true
                """
            }
            
            def open_side_effect(file, mode='r', *args, **kwargs):
                content = mock_files.get(file, "")
                return mock_open(read_data=content).return_value

            with patch("builtins.open", side_effect=open_side_effect):
                 config = load_config()
                 
                 assert config.database.host == "db-yaml-host"
                 assert config.llm.base_url == "http://ollama-yaml:11434"
                 assert config.rag.collection_name == "rag-yaml-collection"
                 assert config.logging["version"] == 1
                 assert config.security["auth"]["enabled"] is True
