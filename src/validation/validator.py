"""
SQL Validator Module
"""
from typing import List, Optional
from ..core.exceptions import SecurityError

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
