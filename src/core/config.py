"""
Configuration Management Module.

Handles loading and validation of application configuration from YAML files
and environment variables.
"""
import os
import re
from typing import Any, Dict, Optional, Match

import yaml
from pydantic import BaseModel, Field

from ..database.models import DatabaseConfig
from ..llm.models import LLMConfig
from ..rag.models import RAGConfig
from .exceptions import ConfigurationError


class AppConfig(BaseModel):
    """Application-wide configuration container."""

    database: DatabaseConfig
    llm: LLMConfig
    rag: RAGConfig
    logging: Dict[str, Any] = Field(default_factory=dict)
    security: Dict[str, Any] = Field(default_factory=dict)


def _substitute_env_vars(value: Any) -> Any:
    """
    Recursively substitute environment variables in configuration values.

    Args:
        value: The value to process (string, dict, list, or other).

    Returns:
        The value with environment variables substituted.
    """
    if isinstance(value, str):
        pattern = r'\$\{([^}:]+)(?::([^}]+))?\}'

        def replace(match: Match[str]) -> str:
            var_name = match.group(1)
            default_value = match.group(2)
            return os.getenv(
                var_name,
                default_value if default_value is not None else ""
            )

        return re.sub(pattern, replace, value)
    if isinstance(value, dict):
        return {k: _substitute_env_vars(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_substitute_env_vars(v) for v in value]
    return value


def _load_yaml_file(config_dir: str, filename: str) -> Dict[str, Any]:
    """
    Load a YAML configuration file with environment variable substitution.

    Args:
        config_dir: Directory containing configuration files.
        filename: Name of the YAML file to load.

    Returns:
        Parsed configuration dictionary.

    Raises:
        ConfigurationError: If the file exists but cannot be loaded.
    """
    path = os.path.join(config_dir, filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                return _substitute_env_vars(data)
        except (OSError, yaml.YAMLError) as e:
            raise ConfigurationError(f"Failed to load {filename}: {e}") from e
    return {}


def _load_database_config(
    config_dir: str,
    base_config: DatabaseConfig
) -> DatabaseConfig:
    """Load database configuration from YAML file."""
    db_yaml = _load_yaml_file(config_dir, "database.yaml")
    if "database" not in db_yaml:
        return base_config

    db_data = db_yaml["database"]
    if "sql_server" not in db_data:
        return base_config

    sql_conf = db_data["sql_server"]
    db_dict = base_config.model_dump()

    for key in ("host", "port", "database", "username", "password"):
        if key in sql_conf:
            db_dict[key] = sql_conf[key]

    if "connection_pool" in sql_conf:
        pool_conf = sql_conf["connection_pool"]
        pool_mapping = {
            "min_size": "pool_size",
            "max_overflow": "max_overflow",
            "timeout": "pool_timeout",
            "pool_recycle": "pool_recycle"
        }
        for src, dest in pool_mapping.items():
            if src in pool_conf:
                db_dict[dest] = pool_conf[src]

    return DatabaseConfig(**db_dict)


def _load_llm_config(config_dir: str, base_config: LLMConfig) -> LLMConfig:
    """Load LLM configuration from YAML file."""
    llm_yaml = _load_yaml_file(config_dir, "ollama.yaml")
    if "ollama" not in llm_yaml:
        return base_config

    ollama_conf = llm_yaml["ollama"]
    llm_dict = base_config.model_dump()

    for key in ("base_url", "timeout"):
        if key in ollama_conf:
            llm_dict[key] = ollama_conf[key]

    if "model" in ollama_conf:
        model_conf = ollama_conf["model"]
        model_mapping = {
            "name": "model_name",
            "temperature": "temperature",
            "max_tokens": "max_tokens",
            "top_p": "top_p"
        }
        for src, dest in model_mapping.items():
            if src in model_conf:
                llm_dict[dest] = model_conf[src]

    if "retry" in ollama_conf and "max_attempts" in ollama_conf["retry"]:
        llm_dict["retry_attempts"] = ollama_conf["retry"]["max_attempts"]

    return LLMConfig(**llm_dict)


def _load_rag_config(config_dir: str, base_config: RAGConfig) -> RAGConfig:
    """Load RAG configuration from YAML file."""
    rag_yaml = _load_yaml_file(config_dir, "rag.yaml")
    if "rag" not in rag_yaml:
        return base_config

    rag_data = rag_yaml["rag"]
    rag_dict = base_config.model_dump()

    if "vector_store" in rag_data:
        vs_conf = rag_data["vector_store"]
        for key in ("persist_directory", "collection_name"):
            if key in vs_conf:
                rag_dict[key] = vs_conf[key]

        if "embedding" in vs_conf:
            rag_dict["embedding_model"] = vs_conf["embedding"].get(
                "model", rag_dict["embedding_model"]
            )

        if "search" in vs_conf:
            search_conf = vs_conf["search"]
            for key in ("top_k", "similarity_threshold"):
                if key in search_conf:
                    rag_dict[key] = search_conf[key]

    return RAGConfig(**rag_dict)


def _apply_config_file_overrides(
    config_path: str,
    config_data: Dict[str, Any]
) -> None:
    """Apply overrides from a specific configuration file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        file_data = yaml.safe_load(f)

    if not file_data:
        return

    if "database" in file_data:
        db_dict = config_data["database"].model_dump()
        db_dict.update(file_data["database"])
        config_data["database"] = DatabaseConfig(**db_dict)

    if "llm" in file_data:
        llm_dict = config_data["llm"].model_dump()
        llm_dict.update(file_data["llm"])
        config_data["llm"] = LLMConfig(**llm_dict)

    if "rag" in file_data:
        rag_dict = config_data["rag"].model_dump()
        rag_dict.update(file_data["rag"])
        config_data["rag"] = RAGConfig(**rag_dict)

    for key in ("logging", "security"):
        if key in file_data:
            config_data[key] = file_data[key]


def _get_db_port() -> int:
    """
    Get database port from environment variable with validation.

    Returns:
        Port number as integer.

    Raises:
        ConfigurationError: If port value is not a valid integer.
    """
    port_str = os.getenv("DB_PORT", "1433")
    try:
        return int(port_str)
    except ValueError as e:
        raise ConfigurationError(
            f"Invalid DB_PORT value '{port_str}': must be an integer"
        ) from e


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    Load configuration from YAML files and environment variables.

    Configuration is loaded from multiple sources in the following order:
    1. Default values from environment variables
    2. YAML files in the config/ directory
    3. Optional override file specified by config_path

    Args:
        config_path: Optional path to a configuration override file.

    Returns:
        AppConfig object containing all configuration.

    Raises:
        ConfigurationError: If configuration is invalid or cannot be loaded.
    """
    # Default values from environment
    db_config = DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=_get_db_port(),
        database=os.getenv("DB_NAME", "MedicalDB"),
        username=os.getenv("DB_USER", "sa"),
        password=os.getenv("DB_PASSWORD", ""),
        type=os.getenv("DB_TYPE", "sqlserver")
    )

    llm_config = LLMConfig()
    rag_config = RAGConfig()
    config_dir = "config"

    try:
        # Load from YAML files
        db_config = _load_database_config(config_dir, db_config)
        llm_config = _load_llm_config(config_dir, llm_config)
        rag_config = _load_rag_config(config_dir, rag_config)

        # Load logging and security
        logging_yaml = _load_yaml_file(config_dir, "logging.yaml")
        security_yaml = _load_yaml_file(config_dir, "security.yaml")

        config_data: Dict[str, Any] = {
            "database": db_config,
            "llm": llm_config,
            "rag": rag_config,
            "logging": logging_yaml.get("logging", {}),
            "security": security_yaml.get("security", {})
        }

        # Override with specific config file if provided
        if config_path and os.path.exists(config_path):
            _apply_config_file_overrides(config_path, config_data)

    except (OSError, yaml.YAMLError) as e:
        raise ConfigurationError(f"Failed to load configuration: {e}") from e

    # Final validation
    try:
        app_config = AppConfig(**config_data)

        # Specific business rule validation
        if app_config.database.type != "sqlite" and not app_config.database.password:
            raise ValueError(
                "Database password is required (DB_PASSWORD env var or config file)."
            )

        return app_config
    except Exception as e:
        raise ConfigurationError(f"Configuration validation failed: {e}") from e
