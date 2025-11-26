"""
Configuration Management Module
"""
import os
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
    )
    
    llm_config = LLMConfig()
    rag_config = RAGConfig()
    
    config_data = {
        "database": db_config,
        "llm": llm_config,
        "rag": rag_config,
        "logging": {}
    }

    # Override with file config if provided
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                file_data = yaml.safe_load(f)
                if file_data:
                    # Deep merge or update logic here
                    # For simplicity, we'll just update the dicts if keys exist
                    if "database" in file_data:
                        # We need to be careful with Pydantic models, 
                        # usually we'd parse the dict into the model
                        # But since we already have models with env vars, 
                        # we might want to prefer file over env or vice versa.
                        # Let's assume file overrides env for explicit values.
                        db_dict = db_config.dict()
                        db_dict.update(file_data["database"])
                        config_data["database"] = DatabaseConfig(**db_dict)
                        
                    if "llm" in file_data:
                        llm_dict = llm_config.dict()
                        llm_dict.update(file_data["llm"])
                        config_data["llm"] = LLMConfig(**llm_dict)
                        
                    if "rag" in file_data:
                        rag_dict = rag_config.dict()
                        rag_dict.update(file_data["rag"])
                        config_data["rag"] = RAGConfig(**rag_dict)
                        
                    if "logging" in file_data:
                        config_data["logging"] = file_data["logging"]
                        
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration file: {e}")

    # Final Validation
    try:
        app_config = AppConfig(**config_data)
        
        # Specific business rule validation
        if app_config.database.type != "sqlite" and not app_config.database.password:
             raise ValueError("Database password is required (DB_PASSWORD env var or config file).")
             
        return app_config
    except Exception as e:
        raise ConfigurationError(f"Configuration validation failed: {e}")
