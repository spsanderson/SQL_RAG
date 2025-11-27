"""
SQL Server Adapter.

SQLAlchemy-based adapter for SQL Server database connections.
"""
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, URL

from ..models import DatabaseConfig
from .sqlalchemy_adapter import SQLAlchemyAdapter


class SQLServerAdapter(SQLAlchemyAdapter):
    """SQL Server implementation of the BaseAdapter using SQLAlchemy."""

    def __init__(self, config: DatabaseConfig):
        """
        Initialize the SQL Server adapter.

        Args:
            config: Database configuration.
        """
        super().__init__(config)
        self._engine: Optional[Engine] = None
        self._connection_string = self._build_connection_string()

    def _build_connection_string(self) -> URL:
        """
        Build the SQLAlchemy connection string for SQL Server.

        Returns:
            SQLAlchemy URL object for the connection.
        """
        connection_url = URL.create(
            "mssql+pyodbc",
            username=self.config.username,
            password=self.config.password,
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            query={"driver": self.config.driver}
        )
        return connection_url

    def connect(self) -> Engine:
        """
        Create and return the SQLAlchemy engine.

        Returns:
            SQLAlchemy Engine instance.
        """
        if not self._engine:
            self._engine = create_engine(
                self._connection_string,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle
            )
        return self._engine
