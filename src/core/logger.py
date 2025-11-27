"""
Logging Configuration Module
"""
import logging
import logging.config
import os
import sys
from typing import Optional, List, Dict, Any

def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    Configure the root logger.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to a log file.
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')

    handlers: List[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers
    )

def configure_logging(config: Dict[str, Any]) -> None:
    """
    Configure logging using a dictionary configuration.
    
    Args:
        config: Dictionary containing logging configuration.
    """
    # Ensure log directory exists if specified in handlers
    if 'handlers' in config:
        for handler in config['handlers'].values():
            if 'filename' in handler:
                log_dir = os.path.dirname(handler['filename'])
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)

    logging.config.dictConfig(config)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Name of the logger (usually __name__)

    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)
