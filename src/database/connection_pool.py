"""
Connection Pool Manager
"""
from typing import Optional
from sqlalchemy.engine import Engine
from .models import DatabaseConfig
from .adapters.sqlserver_adapter import SQLServerAdapter
from .adapters.sqlite_adapter import SQLiteAdapter
from .adapters.base_adapter import BaseAdapter

class ConnectionPool:
    """
    Manages database connections using the appropriate adapter.
    """

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._adapter: BaseAdapter
        if self.config.type == "sqlite":
            self._adapter = SQLiteAdapter(config)
        else:
            self._adapter = SQLServerAdapter(config)
        self._engine: Optional[Engine] = None

    def get_engine(self) -> Engine:
        """
        Get the SQLAlchemy engine from the adapter.
        """
        self._engine = self._adapter.connect()
        return self._engine

    def get_adapter(self) -> BaseAdapter:
        """
        Get the underlying adapter instance.
        """
        return self._adapter

    def dispose(self):
        """
        Dispose of the connection pool.
        """
        if self._engine:
            self._engine.dispose()
