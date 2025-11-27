"""
Base Database Adapter.

Defines the abstract interface for database adapters.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..models import DatabaseConfig, QueryResult, SchemaElement


class BaseAdapter(ABC):
    """Abstract base class for database adapters."""

    def __init__(self, config: DatabaseConfig):
        """
        Initialize the adapter.

        Args:
            config: Database configuration.
        """
        self.config = config

    @abstractmethod
    def connect(self) -> Any:
        """Establish a connection to the database."""
        ...

    @abstractmethod
    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None
    ) -> QueryResult:
        """Execute a SQL query and return the result."""
        ...

    @abstractmethod
    def get_schema(self) -> List[SchemaElement]:
        """Retrieve the database schema."""
        ...

    @abstractmethod
    def validate_connection(self) -> bool:
        """Validate that the connection is working."""
        ...
