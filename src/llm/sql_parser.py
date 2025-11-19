"""
SQL Parser Service
"""
import re

class SQLParser:
    """
    Parses SQL queries from LLM responses.
    """
    
    def parse(self, llm_response: str) -> str:
        """
        Extract the SQL query from the LLM response.
        Handles markdown code blocks and raw text.
        """
        # Remove markdown code blocks
        sql_match = re.search(r"```sql\n(.*?)\n```", llm_response, re.DOTALL)
        if sql_match:
            return sql_match.group(1).strip()
        
        # Try generic code block
        code_match = re.search(r"```\n(.*?)\n```", llm_response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
            
        # Assume raw text is the query if no blocks found
        # But clean up any leading/trailing whitespace or common prefixes
        cleaned = llm_response.strip()
        
        # Remove "SQL Query:" prefix if present
        if cleaned.lower().startswith("sql query:"):
            cleaned = cleaned[10:].strip()
            
        return cleaned
