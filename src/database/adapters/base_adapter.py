"""
Base Database Adapter
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from ..models import DatabaseConfig, QueryResult, SchemaElement

class BaseAdapter(ABC):
    """
    Abstract base class for database adapters.
    """

    def __init__(self, config: DatabaseConfig):
        self.config = config

    @abstractmethod
    def connect(self) -> Any:
        """
        Establish a connection to the database.
        """
        pass

    @abstractmethod
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None, timeout: Optional[int] = None) -> QueryResult:
        """
        Execute a SQL query and return the result.
        """
        pass

    @abstractmethod
    def get_schema(self) -> List[SchemaElement]:
        """
        Retrieve the database schema.
        """
        pass

    @abstractmethod
    def validate_connection(self) -> bool:
        """
        Validate that the connection is working.
        """
        pass
