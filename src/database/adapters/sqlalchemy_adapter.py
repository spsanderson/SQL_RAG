"""
SQLAlchemy Adapter Base Class.

Base implementation for SQLAlchemy-based database adapters.
"""
import time
from typing import Any, Dict, List, Optional

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from ...core.exceptions import DatabaseError
from ..models import QueryResult, SchemaElement
from .base_adapter import BaseAdapter


class SQLAlchemyAdapter(BaseAdapter):
    """Base adapter for SQLAlchemy-based database connections."""

    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None
    ) -> QueryResult:
        """
        Execute a SQL query and return the result.

        Args:
            query: SQL query to execute.
            params: Optional query parameters.
            timeout: Optional timeout in seconds.

        Returns:
            QueryResult containing the query results.

        Raises:
            DatabaseError: If query execution fails.
        """
        engine = self.connect()
        start_time = time.time()

        query_timeout = (
            timeout if timeout is not None else self.config.pool_timeout
        )

        try:
            with engine.connect() as connection:
                connection = connection.execution_options(timeout=query_timeout)
                with connection.begin():
                    result = connection.execute(text(query), params or {})

                if result.returns_rows:
                    columns = list(result.keys())
                    # Access _mapping for row dict conversion
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
            raise DatabaseError(f"Database execution error: {e}") from e

    def get_schema(self) -> List[SchemaElement]:
        """
        Retrieve the database schema using SQLAlchemy inspector.

        Returns:
            List of schema elements (tables and columns).
        """
        engine = self.connect()
        inspector = inspect(engine)
        schema_elements = []

        for table_name in inspector.get_table_names():
            schema_elements.append(SchemaElement(
                name=table_name,
                type="table",
                description=f"Table: {table_name}"
            ))

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

        Returns:
            True if connection is valid, False otherwise.
        """
        try:
            engine = self.connect()
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError:
            return False
