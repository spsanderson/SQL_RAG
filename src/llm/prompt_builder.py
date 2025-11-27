"""
Prompt Builder Service.

Builds prompts for the LLM by combining schema context, user questions,
and conversation history.
"""
from typing import Any, Dict, List, Optional

from ..database.models import SchemaElement


class PromptBuilder:
    """Builds prompts for the LLM."""

    DEFAULT_TEMPLATE = """
You are an expert SQL developer. Your goal is to write a correct and \
efficient {dialect} query to answer the user's question.

### Database Schema
The following tables and columns are available:
{schema_context}

### Instructions
1. Return ONLY the SQL query.
2. Do not include any explanations or markdown formatting.
3. Use {dialect} syntax.
4. If the question cannot be answered with the given schema, return "NO_SQL".

### User Question
{user_question}

### Chat History
{chat_history}

### SQL Query
"""

    def __init__(self, dialect: str = "T-SQL"):
        """
        Initialize the prompt builder.

        Args:
            dialect: SQL dialect to use (e.g., "T-SQL", "SQLite").
        """
        self.dialect = dialect

    def build_prompt(
        self,
        user_question: str,
        schema_elements: Optional[List[SchemaElement]] = None,
        context_str: Optional[str] = None,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Construct the prompt with schema context, user question, and history.

        Args:
            user_question: The user's natural language question.
            schema_elements: Optional list of schema elements for context.
            context_str: Optional pre-formatted context string.
            history: Optional list of chat history messages.

        Returns:
            Formatted prompt string.

        Raises:
            ValueError: If user question is empty or too long.
        """
        if not user_question or not user_question.strip():
            raise ValueError("User question cannot be empty.")

        if len(user_question) > 500:
            raise ValueError("User question is too long (max 500 characters).")

        if context_str:
            schema_context = context_str
        elif schema_elements:
            schema_context = self._format_schema(schema_elements)
        else:
            schema_context = "No schema information provided."

        history_str = self._format_history(history)

        return self.DEFAULT_TEMPLATE.format(
            dialect=self.dialect,
            schema_context=schema_context,
            user_question=user_question,
            chat_history=history_str
        )

    def _format_history(
        self,
        history: Optional[List[Dict[str, Any]]]
    ) -> str:
        """
        Format chat history into a string representation.

        Args:
            history: List of message dictionaries with 'role' and 'content'.

        Returns:
            Formatted history string.
        """
        if not history:
            return "No previous conversation."

        recent_history = history[-5:]
        lines = []
        for msg in recent_history:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            lines.append(f"{role}: {content}")

        return "\n".join(lines)

    def _format_schema(self, schema_elements: List[SchemaElement]) -> str:
        """
        Format schema elements into a string representation.

        Args:
            schema_elements: List of schema elements to format.

        Returns:
            Formatted schema string.
        """
        tables: Dict[str, List[str]] = {}
        for element in schema_elements:
            if element.type == 'table':
                tables[element.name] = []
            elif element.type == 'column' and element.metadata:
                table_name = element.metadata.get('table')
                if table_name:
                    if table_name not in tables:
                        tables[table_name] = []
                    dtype = element.metadata.get('dtype', 'unknown')
                    tables[table_name].append(f"{element.name} ({dtype})")

        formatted_lines = []
        for table, columns in tables.items():
            formatted_lines.append(f"- Table: {table}")
            for col in columns:
                formatted_lines.append(f"  - {col}")

        return "\n".join(formatted_lines)
