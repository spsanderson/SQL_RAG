"""
Unit tests for Config.

Tests cover loading configuration from environment variables, YAML files,
and validation of configuration values.
"""
import os

import pytest
from unittest.mock import patch, mock_open

from src.core.config import load_config
from src.core.exceptions import ConfigurationError


def test_load_config_defaults():
    """Test loading configuration with default values."""
    with patch.dict(os.environ, {"DB_PASSWORD": "default-password"}, clear=True):
        config = load_config()
        assert config.database.host == "localhost"
        assert config.database.type == "sqlserver"


def test_load_config_env_vars():
    """Test loading configuration from environment variables."""
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
    """Test loading configuration from a YAML file."""
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
    """Test that missing password for non-sqlite database raises error."""
    with patch.dict(os.environ, {"DB_TYPE": "sqlserver"}, clear=True):
        with pytest.raises(Exception):  # ConfigurationError or ValueError
            load_config()


def test_load_config_invalid_port():
    """Test that invalid DB_PORT value raises ConfigurationError."""
    env_vars = {
        "DB_PORT": "not-a-number",
        "DB_PASSWORD": "test-password"
    }
    with patch.dict(os.environ, env_vars, clear=True):
        with pytest.raises(ConfigurationError) as exc_info:
            load_config()
        assert "Invalid DB_PORT value" in str(exc_info.value)


def test_load_multiple_configs():
    """Test loading configuration from multiple YAML files."""
    with patch.dict(os.environ, {"DB_PASSWORD": "env-password"}, clear=True):
        with patch("os.path.exists") as mock_exists:
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
