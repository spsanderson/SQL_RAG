"""
SQL Validator Module
"""
import re
from typing import List, Optional, Set
from ..core.exceptions import SecurityError
from ..database.models import SchemaElement

class SQLValidator:
    """
    Validates SQL queries to prevent security vulnerabilities and prohibited operations.
    """

    # Prohibited keywords (case-insensitive)
    PROHIBITED_KEYWORDS = {
        'DROP', 'ALTER', 'CREATE', 'TRUNCATE',
        'INSERT', 'UPDATE', 'DELETE', 'MERGE',
        'GRANT', 'REVOKE',
        'XP_CMDSHELL', 'SP_EXECUTESQL'
    }

    def __init__(self, schema: Optional[List[SchemaElement]] = None):
        """
        Initialize the validator.

        Args:
            schema: Optional list of schema elements to validate against.
        """
        self.schema = schema
        self.table_names = {e.name.upper() for e in schema if e.type == 'table'} if schema else set()

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

        # Normalize query for checking
        normalized_query = query.upper()

        # Check for prohibited keywords
        # We look for whole words to avoid false positives (e.g., "UPDATE_DATE" column)
        for keyword in self.PROHIBITED_KEYWORDS:
            # Regex to match whole word, allowing for boundaries like whitespace, parens, semicolons
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, normalized_query):
                raise SecurityError(f"Query contains prohibited keyword: {keyword}")

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
        if not self.schema:
            return True

        # Simple regex to find table names in FROM/JOIN clauses
        # This is not a full SQL parser but covers common cases
        # Matches: FROM table_name, JOIN table_name
        # We assume table names are alphanumeric + underscores
        normalized_query = query.upper()

        # Find all words after FROM or JOIN
        # Pattern: (FROM|JOIN)\s+([A-Z0-9_]+)
        pattern = r'(?:FROM|JOIN)\s+([A-Z0-9_]+)'
        matches = re.findall(pattern, normalized_query)

        for table in matches:
            if table not in self.table_names:
                # Check if it's a known alias or subquery (hard to do with regex)
                # For now, we'll be strict. If it's not in schema, it's flagged.
                # To avoid false positives with subqueries/aliases, we might need a real parser.
                # But for this requirement, we'll start with this.
                raise SecurityError(f"Query references invalid table: {table}")

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
            raise SecurityError(f"Query too complex: {join_count} JOINs (max 5)")

        # Count subqueries (approximate by counting SELECTs - 1)
        select_count = len(re.findall(r'\bSELECT\b', normalized_query))
        if select_count > 3:
             raise SecurityError(f"Query too complex: {select_count} SELECT statements (max 3)")

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

        # Check for TOP or LIMIT
        has_top = 'TOP' in normalized_query
        has_limit = 'LIMIT' in normalized_query

        # Check for COUNT which implies a single row result
        is_count = 'COUNT(' in normalized_query

        if not (has_top or has_limit or is_count):
            raise SecurityError("Query must include a result limit (TOP or LIMIT) or be an aggregation.")

        return True
