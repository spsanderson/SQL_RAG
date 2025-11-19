"""
Prompt Builder Service
"""
from typing import List, Optional
from ..database.models import SchemaElement

class PromptBuilder:
    """
    Builds prompts for the LLM.
    """
    
    DEFAULT_TEMPLATE = """
You are an expert SQL developer. Your goal is to write a correct and efficient T-SQL query to answer the user's question.

### Database Schema
The following tables and columns are available:
{schema_context}

### Instructions
1. Return ONLY the SQL query.
2. Do not include any explanations or markdown formatting.
3. Use T-SQL syntax (SQL Server).
4. If the question cannot be answered with the given schema, return "NO_SQL".

### User Question
{user_question}

### SQL Query
"""

    def build_prompt(self, user_question: str, schema_elements: List[SchemaElement]) -> str:
        """
        Construct the prompt with schema context and user question.
        """
        schema_context = self._format_schema(schema_elements)
        return self.DEFAULT_TEMPLATE.format(
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
