"""
Configuration Management Module
"""
import os
import re
import yaml
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from ..database.models import DatabaseConfig
from ..llm.models import LLMConfig
from ..rag.models import RAGConfig
from .exceptions import ConfigurationError

class AppConfig(BaseModel):
    """
    Application-wide configuration.
    """
    database: DatabaseConfig
    llm: LLMConfig
    rag: RAGConfig
    logging: Dict[str, Any] = Field(default_factory=dict)
    security: Dict[str, Any] = Field(default_factory=dict)

def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    Load configuration from YAML file and environment variables.

    Args:
        config_path: Path to the configuration file.

    Returns:
        AppConfig object.

    Raises:
        ConfigurationError: If configuration is invalid.
    """
    # Default values from environment
    db_config = DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 1433)),
        database=os.getenv("DB_NAME", "MedicalDB"),
        username=os.getenv("DB_USER", "sa"),
        password=os.getenv("DB_PASSWORD", ""), # Empty default, validation happens later
        type=os.getenv("DB_TYPE", "sqlserver")
    ) # type: ignore

    llm_config = LLMConfig() # type: ignore
    rag_config = RAGConfig() # type: ignore

    config_data = {
        "database": db_config,
        "llm": llm_config,
        "rag": rag_config,
        "logging": {},
        "security": {}
    }

    # Load specific config files
    config_dir = "config"
    
    def substitute_env_vars(value: Any) -> Any:
        if isinstance(value, str):
            # Regex to match ${VAR} or ${VAR:default}
            pattern = r'\$\{([^}:]+)(?::([^}]+))?\}'
            def replace(match):
                var_name = match.group(1)
                default_value = match.group(2)
                return os.getenv(var_name, default_value if default_value is not None else "")
            
            # If the entire string is the variable, we might want to cast the result
            # But for now, let's just replace. Pydantic can handle type coercion usually.
            # However, for port (int), "1433" string is fine.
            return re.sub(pattern, replace, value)
        elif isinstance(value, dict):
            return {k: substitute_env_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [substitute_env_vars(v) for v in value]
        return value

    # Helper to load yaml
    def load_yaml(filename: str) -> Dict[str, Any]:
        path = os.path.join(config_dir, filename)
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = yaml.safe_load(f) or {}
                    return substitute_env_vars(data)
            except (OSError, yaml.YAMLError) as e:
                # Log warning but continue? Or raise?
                # For now, let's raise as these are expected to be valid if present
                raise ConfigurationError(f"Failed to load {filename}: {e}")
        return {}

    # Load and merge configurations
    try:
        # Database
        db_yaml = load_yaml("database.yaml")
        if "database" in db_yaml:
            db_data = db_yaml["database"]
            # Handle nested structure for sql_server
            if "sql_server" in db_data:
                sql_conf = db_data["sql_server"]
                # Update flat fields
                db_dict = db_config.dict()
                if "host" in sql_conf: db_dict["host"] = sql_conf["host"]
                if "port" in sql_conf: db_dict["port"] = sql_conf["port"]
                if "database" in sql_conf: db_dict["database"] = sql_conf["database"]
                if "username" in sql_conf: db_dict["username"] = sql_conf["username"]
                if "password" in sql_conf: db_dict["password"] = sql_conf["password"]
                
                if "connection_pool" in sql_conf:
                    pool_conf = sql_conf["connection_pool"]
                    if "min_size" in pool_conf: db_dict["pool_size"] = pool_conf["min_size"]
                    if "max_overflow" in pool_conf: db_dict["max_overflow"] = pool_conf["max_overflow"]
                    if "timeout" in pool_conf: db_dict["pool_timeout"] = pool_conf["timeout"]
                    if "pool_recycle" in pool_conf: db_dict["pool_recycle"] = pool_conf["pool_recycle"]
                
                config_data["database"] = DatabaseConfig(**db_dict)

        # LLM
        llm_yaml = load_yaml("ollama.yaml")
        if "ollama" in llm_yaml:
            ollama_conf = llm_yaml["ollama"]
            llm_dict = llm_config.dict()
            if "base_url" in ollama_conf: llm_dict["base_url"] = ollama_conf["base_url"]
            if "timeout" in ollama_conf: llm_dict["timeout"] = ollama_conf["timeout"]
            
            if "model" in ollama_conf:
                model_conf = ollama_conf["model"]
                if "name" in model_conf: llm_dict["model_name"] = model_conf["name"]
                if "temperature" in model_conf: llm_dict["temperature"] = model_conf["temperature"]
                if "max_tokens" in model_conf: llm_dict["max_tokens"] = model_conf["max_tokens"]
                if "top_p" in model_conf: llm_dict["top_p"] = model_conf["top_p"]
            
            if "retry" in ollama_conf:
                retry_conf = ollama_conf["retry"]
                if "max_attempts" in retry_conf: llm_dict["retry_attempts"] = retry_conf["max_attempts"]
                
            config_data["llm"] = LLMConfig(**llm_dict)

        # RAG
        rag_yaml = load_yaml("rag.yaml")
        if "rag" in rag_yaml:
            rag_data = rag_yaml["rag"]
            rag_dict = rag_config.dict()
            
            if "vector_store" in rag_data:
                vs_conf = rag_data["vector_store"]
                if "persist_directory" in vs_conf: rag_dict["persist_directory"] = vs_conf["persist_directory"]
                if "collection_name" in vs_conf: rag_dict["collection_name"] = vs_conf["collection_name"]
                
                if "embedding" in vs_conf:
                    rag_dict["embedding_model"] = vs_conf["embedding"].get("model", rag_dict["embedding_model"])
                    
                if "search" in vs_conf:
                    search_conf = vs_conf["search"]
                    if "top_k" in search_conf: rag_dict["top_k"] = search_conf["top_k"]
                    if "similarity_threshold" in search_conf: rag_dict["similarity_threshold"] = search_conf["similarity_threshold"]
            
            config_data["rag"] = RAGConfig(**rag_dict)

        # Logging
        logging_yaml = load_yaml("logging.yaml")
        if "logging" in logging_yaml:
            config_data["logging"] = logging_yaml["logging"]

        # Security
        security_yaml = load_yaml("security.yaml")
        if "security" in security_yaml:
            config_data["security"] = security_yaml["security"]

        # Override with specific config file if provided (legacy support)
        if config_path and os.path.exists(config_path):
             with open(config_path, 'r') as f:
                file_data = yaml.safe_load(f)
                if file_data:
                    if "database" in file_data:
                        db_dict = config_data["database"].dict()
                        db_dict.update(file_data["database"])
                        config_data["database"] = DatabaseConfig(**db_dict)
                    if "llm" in file_data:
                        llm_dict = config_data["llm"].dict()
                        llm_dict.update(file_data["llm"])
                        config_data["llm"] = LLMConfig(**llm_dict)
                    if "rag" in file_data:
                        rag_dict = config_data["rag"].dict()
                        rag_dict.update(file_data["rag"])
                        config_data["rag"] = RAGConfig(**rag_dict)
                    if "logging" in file_data:
                        config_data["logging"] = file_data["logging"]
                    if "security" in file_data:
                        config_data["security"] = file_data["security"]

    except (OSError, yaml.YAMLError) as e:
        raise ConfigurationError(f"Failed to load configuration: {e}")

    # Final Validation
    try:
        app_config = AppConfig(**config_data) # type: ignore

        # Specific business rule validation
        if app_config.database.type != "sqlite" and not app_config.database.password:
             raise ValueError("Database password is required (DB_PASSWORD env var or config file).")

        return app_config
    except Exception as e:
        raise ConfigurationError(f"Configuration validation failed: {e}")
