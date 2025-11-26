"""
Prompt Builder Service
"""
from typing import List, Optional
from ..database.models import SchemaElement

class PromptBuilder:
    """
    Builds prompts for the LLM.
    """
    
    def __init__(self, dialect: str = "T-SQL"):
        self.dialect = dialect
        self.DEFAULT_TEMPLATE = """
You are an expert SQL developer. Your goal is to write a correct and efficient {dialect} query to answer the user's question.

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

### SQL Query
"""

    def build_prompt(self, user_question: str, schema_elements: Optional[List[SchemaElement]] = None, context_str: Optional[str] = None) -> str:
        """
        Construct the prompt with schema context and user question.
        """
        # Input Validation
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

        return self.DEFAULT_TEMPLATE.format(
            dialect=self.dialect,
            schema_context=schema_context,
            user_question=user_question
        )

    def _format_schema(self, schema_elements: List[SchemaElement]) -> str:
        """
        Format schema elements into a string representation.
        """
        tables = {}
        for element in schema_elements:
            if element.type == 'table':
                tables[element.name] = []
            elif element.type == 'column':
                table_name = element.metadata.get('table')
                if table_name:
                    if table_name not in tables:
                        tables[table_name] = []
                    tables[table_name].append(f"{element.name} ({element.metadata.get('dtype', 'unknown')})")

        formatted_lines = []
        for table, columns in tables.items():
            formatted_lines.append(f"- Table: {table}")
            for col in columns:
                formatted_lines.append(f"  - {col}")
        
        return "\n".join(formatted_lines)
