"""
SQLite Adapter
"""
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from ..models import DatabaseConfig
from .sqlalchemy_adapter import SQLAlchemyAdapter

class SQLiteAdapter(SQLAlchemyAdapter):
    """
    SQLite implementation of the BaseAdapter using SQLAlchemy.
    """
    
    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self._engine: Optional[Engine] = None
        # For SQLite, we use the database name as the file path
        self._connection_string = f"sqlite:///{self.config.database}"

    def connect(self) -> Engine:
        """
        Create and return the SQLAlchemy engine.
        """
        if not self._engine:
            self._engine = create_engine(
                self._connection_string
            )
        return self._engine


