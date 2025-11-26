"""
SQLAlchemy Adapter Base Class
"""
import time
from typing import List, Optional, Any, Dict
from sqlalchemy import text, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from ..models import DatabaseConfig, QueryResult, SchemaElement
from .base_adapter import BaseAdapter
from ...core.exceptions import DatabaseError

class SQLAlchemyAdapter(BaseAdapter):
    """
    Base adapter for SQLAlchemy-based database connections.
    """
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None, timeout: Optional[int] = None) -> QueryResult:
        """
        Execute a SQL query and return the result.
        """
        engine = self.connect()
        start_time = time.time()
        
        # Use configured timeout if not provided
        query_timeout = timeout if timeout is not None else self.config.pool_timeout
        
        try:
            # Use execution_options for timeout
            # Use execution_options for timeout
            with engine.connect() as connection:
                connection = connection.execution_options(timeout=query_timeout)
                with connection.begin():
                    result = connection.execute(text(query), params or {})
                
                # For SELECT queries, fetch results
                if result.returns_rows:
                    columns = list(result.keys())
                    rows = [dict(row._mapping) for row in result.fetchall()]
                    row_count = len(rows)
                else:
                    columns = []
                    rows = []
                    row_count = result.rowcount

                execution_time = time.time() - start_time
                
                return QueryResult(
                    columns=columns,
                    rows=rows,
                    row_count=row_count,
                    execution_time=execution_time
                )
        except SQLAlchemyError as e:
            raise DatabaseError(f"Database execution error: {str(e)}") from e

    def get_schema(self) -> List[SchemaElement]:
        """
        Retrieve the database schema using SQLAlchemy inspector.
        """
        engine = self.connect()
        inspector = inspect(engine)
        schema_elements = []

        for table_name in inspector.get_table_names():
            # Add table
            schema_elements.append(SchemaElement(
                name=table_name,
                type="table",
                description=f"Table: {table_name}"
            ))
            
            # Add columns
            for column in inspector.get_columns(table_name):
                col_name = column['name']
                col_type = str(column['type'])
                schema_elements.append(SchemaElement(
                    name=f"{table_name}.{col_name}",
                    type="column",
                    description=f"Column: {col_name} ({col_type})",
                    metadata={"table": table_name, "dtype": col_type}
                ))
                
        return schema_elements

    def validate_connection(self) -> bool:
        """
        Validate that the connection is working.
        """
        try:
            engine = self.connect()
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
