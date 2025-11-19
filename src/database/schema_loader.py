"""
Schema Loader Service
"""
from typing import List
from .connection_pool import ConnectionPool
from .models import SchemaElement

class SchemaLoader:
    """
    Loads and caches database schema information.
    """
    
    def __init__(self, pool: ConnectionPool):
        self.pool = pool

    def load_schema(self) -> List[SchemaElement]:
        """
        Load the current database schema.
        """
        adapter = self.pool.get_adapter()
        return adapter.get_schema()
