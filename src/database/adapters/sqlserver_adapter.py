"""
SQL Server Adapter
"""
import time
from typing import List, Optional, Any, Dict
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.exc import SQLAlchemyError

from ..models import DatabaseConfig, QueryResult, SchemaElement
from .base_adapter import BaseAdapter

class SQLServerAdapter(BaseAdapter):
    """
    SQL Server implementation of the BaseAdapter using SQLAlchemy.
    """
    
    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self._engine: Optional[Engine] = None
        self._connection_string = self._build_connection_string()

    def _build_connection_string(self) -> str:
        """
        Build the SQLAlchemy connection string for SQL Server.
        """
        # Using mssql+pyodbc dialect
        return (
            f"mssql+pyodbc://{self.config.username}:{self.config.password}"
            f"@{self.config.host}:{self.config.port}/{self.config.database}"
            f"?driver={self.config.driver.replace(' ', '+')}"
        )

    def connect(self) -> Engine:
        """
        Create and return the SQLAlchemy engine.
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

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> QueryResult:
        """
        Execute a SQL query and return the result.
        """
        engine = self.connect()
        start_time = time.time()
        
        try:
            with engine.connect() as connection:
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
            # In a real app, we might want to wrap this in a custom exception
            raise Exception(f"Database execution error: {str(e)}") from e

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
