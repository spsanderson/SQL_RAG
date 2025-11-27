"""
SQL Validator Module.

Validates SQL queries to prevent security vulnerabilities and ensure
queries only reference valid database objects.
"""
import json
import re
from typing import Any, Dict, List, Optional, Set

from ..core.exceptions import SecurityError
from ..database.models import SchemaElement


class SQLValidator:
    """
    Validates SQL queries to prevent security vulnerabilities and prohibited operations.

    Supports validation against:
    - Prohibited SQL keywords (DML/DDL/DCL operations)
    - Database schema (tables and columns)
    - Query complexity limits
    - Result set limits
    """

    # Prohibited keywords (case-insensitive)
    PROHIBITED_KEYWORDS: Set[str] = {
        'DROP', 'ALTER', 'CREATE', 'TRUNCATE',
        'INSERT', 'UPDATE', 'DELETE', 'MERGE',
        'GRANT', 'REVOKE',
        'XP_CMDSHELL', 'SP_EXECUTESQL'
    }

    def __init__(
        self,
        schema: Optional[List[SchemaElement]] = None,
        schema_json_path: Optional[str] = None
    ):
        """
        Initialize the validator.

        Args:
            schema: Optional list of schema elements to validate against.
            schema_json_path: Optional path to a JSON schema file for validation.
        """
        self.schema = schema
        self._table_names: Set[str] = set()
        self._column_map: Dict[str, Set[str]] = {}

        if schema:
            self._load_from_schema_elements(schema)
        elif schema_json_path:
            self._load_from_json(schema_json_path)

    def _load_from_schema_elements(
        self,
        schema: List[SchemaElement]
    ) -> None:
        """Load schema information from SchemaElement list."""
        for element in schema:
            if element.type == 'table':
                self._table_names.add(element.name.upper())
                self._column_map[element.name.upper()] = set()
            elif element.type == 'column' and element.metadata:
                table_name = element.metadata.get('table', '').upper()
                if table_name:
                    if table_name not in self._column_map:
                        self._column_map[table_name] = set()
                    # Extract column name from "table.column" format
                    col_name = element.name.split('.')[-1].upper()
                    self._column_map[table_name].add(col_name)

    def _load_from_json(self, schema_json_path: str) -> None:
        """
        Load schema information from a JSON file.

        The JSON file should have the format:
        {
            "TableName": {
                "columns": [
                    {"name": "column_name", "type": "type", ...},
                    ...
                ],
                "foreign_keys": [...]
            },
            ...
        }

        Args:
            schema_json_path: Path to the JSON schema file.

        Raises:
            SecurityError: If the schema file cannot be loaded.
        """
        try:
            with open(schema_json_path, 'r', encoding='utf-8') as f:
                schema_data: Dict[str, Any] = json.load(f)

            for table_name, table_info in schema_data.items():
                upper_table = table_name.upper()
                self._table_names.add(upper_table)
                self._column_map[upper_table] = set()

                if isinstance(table_info, dict) and 'columns' in table_info:
                    for column in table_info['columns']:
                        if isinstance(column, dict) and 'name' in column:
                            self._column_map[upper_table].add(
                                column['name'].upper()
                            )

        except (OSError, json.JSONDecodeError) as e:
            raise SecurityError(f"Failed to load schema file: {e}") from e

    @property
    def table_names(self) -> Set[str]:
        """Get the set of valid table names."""
        return self._table_names

    @property
    def column_map(self) -> Dict[str, Set[str]]:
        """Get the mapping of table names to column names."""
        return self._column_map

    def validate_query(self, query: str) -> bool:
        """
        Validate a SQL query against security rules.

        Args:
            query: The SQL query string to validate.

        Returns:
            True if valid.

        Raises:
            SecurityError: If the query contains prohibited keywords or patterns.
        """
        if not query or not query.strip():
            raise SecurityError("Query cannot be empty.")

        normalized_query = query.upper()

        # Check for prohibited keywords using word boundaries
        for keyword in self.PROHIBITED_KEYWORDS:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, normalized_query):
                raise SecurityError(
                    f"Query contains prohibited keyword: {keyword}"
                )

        return True

    def validate_schema(self, query: str) -> bool:
        """
        Validate that tables used in the query exist in the schema.

        Args:
            query: The SQL query.

        Returns:
            True if valid.

        Raises:
            SecurityError: If an invalid table is referenced.
        """
        if not self._table_names:
            return True

        normalized_query = query.upper()

        # Find table names after FROM or JOIN
        pattern = r'(?:FROM|JOIN)\s+([A-Z0-9_]+)'
        matches = re.findall(pattern, normalized_query)

        for table in matches:
            if table not in self._table_names:
                raise SecurityError(
                    f"Query references invalid table: {table}"
                )

        return True

    def validate_columns(self, query: str) -> bool:
        """
        Validate that columns used in the query exist in their respective tables.

        This method performs a best-effort validation of column references.
        It may not catch all invalid references due to the complexity of
        SQL parsing without a full parser.

        Args:
            query: The SQL query.

        Returns:
            True if valid or if column validation is not possible.

        Raises:
            SecurityError: If a clearly invalid column reference is detected.
        """
        if not self._column_map:
            return True

        normalized_query = query.upper()

        # Find explicit table.column references
        pattern = r'([A-Z0-9_]+)\.([A-Z0-9_]+)'
        matches = re.findall(pattern, normalized_query)

        for table, column in matches:
            if table in self._column_map:
                if column not in self._column_map[table]:
                    raise SecurityError(
                        f"Query references invalid column: {table}.{column}"
                    )

        return True

    def validate_complexity(self, query: str) -> bool:
        """
        Validate query complexity.

        Args:
            query: The SQL query.

        Returns:
            True if valid.

        Raises:
            SecurityError: If query is too complex.
        """
        normalized_query = query.upper()

        # Count JOINs
        join_count = len(re.findall(r'\bJOIN\b', normalized_query))
        if join_count > 5:
            raise SecurityError(
                f"Query too complex: {join_count} JOINs (max 5)"
            )

        # Count subqueries (approximate by counting SELECTs - 1)
        select_count = len(re.findall(r'\bSELECT\b', normalized_query))
        if select_count > 3:
            raise SecurityError(
                f"Query too complex: {select_count} SELECT statements (max 3)"
            )

        return True

    def enforce_result_limit(self, query: str) -> bool:
        """
        Check if result limit is present.

        Args:
            query: The SQL query.

        Returns:
            True if valid.

        Raises:
            SecurityError: If no limit is specified.
        """
        normalized_query = query.upper()

        has_top = 'TOP' in normalized_query
        has_limit = 'LIMIT' in normalized_query
        is_count = 'COUNT(' in normalized_query

        if not (has_top or has_limit or is_count):
            raise SecurityError(
                "Query must include a result limit (TOP or LIMIT) "
                "or be an aggregation."
            )

        return True
