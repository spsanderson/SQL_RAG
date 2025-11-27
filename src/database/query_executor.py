"""
Query Executor Service.

Provides an interface for executing SQL queries against the database.
"""
from typing import Any, Dict, Optional

from .connection_pool import ConnectionPool
from .models import QueryResult


class QueryExecutor:
    """Executes SQL queries against the database using the connection pool."""

    def __init__(self, pool: ConnectionPool):
        """
        Initialize the query executor.

        Args:
            pool: Connection pool for database access.
        """
        self.pool = pool

    def execute(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None
    ) -> QueryResult:
        """
        Execute a query and return the results.

        Args:
            query: SQL query to execute.
            params: Optional query parameters.
            timeout: Optional timeout in seconds.

        Returns:
            QueryResult containing the query results.
        """
        adapter = self.pool.get_adapter()
        return adapter.execute_query(query, params, timeout)

    def validate_connection(self) -> bool:
        """
        Check if the database connection is valid.

        Returns:
            True if connection is valid, False otherwise.
        """
        adapter = self.pool.get_adapter()
        return adapter.validate_connection()
