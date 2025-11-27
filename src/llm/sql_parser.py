"""
SQL Parser Service.

Extracts SQL queries from LLM responses, handling various formats
including markdown code blocks and raw text.
"""
import re


class SQLParser:
    """Parses SQL queries from LLM responses."""

    def parse(self, llm_response: str) -> str:
        """
        Extract the SQL query from the LLM response.

        Handles multiple formats:
        - Markdown SQL code blocks (```sql ... ```)
        - Generic markdown code blocks (``` ... ```)
        - Raw text with optional "SQL Query:" prefix
        - Text with HTML-like tags

        Args:
            llm_response: The raw response from the LLM.

        Returns:
            The extracted SQL query string.
        """
        # Try markdown SQL code block first
        sql_match = re.search(r"```sql\n(.*?)\n```", llm_response, re.DOTALL)
        if sql_match:
            return sql_match.group(1).strip()

        # Try generic code block
        code_match = re.search(r"```\n(.*?)\n```", llm_response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()

        # Clean up raw text
        cleaned = llm_response.strip()

        # Remove "SQL Query:" prefix if present
        if cleaned.lower().startswith("sql query:"):
            cleaned = cleaned[10:].strip()

        # Remove HTML-like tags (e.g., </start_of_turn>)
        cleaned = re.sub(r"<.*?>", "", cleaned).strip()

        return cleaned
