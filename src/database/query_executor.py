"""
Query Executor Service
"""
from typing import Optional, Dict, Any
from .connection_pool import ConnectionPool
from .models import QueryResult

class QueryExecutor:
    """
    Executes SQL queries against the database using the connection pool.
    """

    def __init__(self, pool: ConnectionPool):
        self.pool = pool

    def execute(self, query: str, params: Optional[Dict[str, Any]] = None, timeout: Optional[int] = None) -> QueryResult:
        """
        Execute a query and return the results.
        """
        adapter = self.pool.get_adapter()
        return adapter.execute_query(query, params, timeout)

    def validate_connection(self) -> bool:
        """
        Check if the database connection is valid.
        """
        adapter = self.pool.get_adapter()
        return adapter.validate_connection()
