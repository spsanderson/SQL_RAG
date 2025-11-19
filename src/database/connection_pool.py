"""
Connection Pool Manager
"""
from typing import Optional
from sqlalchemy.engine import Engine
from .models import DatabaseConfig
from .adapters.sqlserver_adapter import SQLServerAdapter

class ConnectionPool:
    """
    Manages database connections using the appropriate adapter.
    """
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._adapter = SQLServerAdapter(config) # Currently hardcoded to SQL Server
        self._engine: Optional[Engine] = None

    def get_engine(self) -> Engine:
        """
        Get the SQLAlchemy engine from the adapter.
        """
        return self._adapter.connect()

    def get_adapter(self) -> SQLServerAdapter:
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
