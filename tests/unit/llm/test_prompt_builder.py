"""
Test Prompt Builder
"""
import pytest
from src.llm.prompt_builder import PromptBuilder
from src.database.models import SchemaElement

def test_build_prompt_formats_correctly():
    """
    Test that the prompt is constructed with the correct context and question.
    """
    builder = PromptBuilder()
    schema = [
        SchemaElement(name="users", type="table"),
        SchemaElement(name="users.id", type="column", metadata={"table": "users", "dtype": "INTEGER"}),
        SchemaElement(name="users.name", type="column", metadata={"table": "users", "dtype": "VARCHAR"})
    ]
    question = "How many users are there?"
    
    prompt = builder.build_prompt(question, schema)
    
    assert "How many users are there?" in prompt
    assert "- Table: users" in prompt
    assert "  - users.id (INTEGER)" in prompt
    assert "  - users.name (VARCHAR)" in prompt
    assert "You are an expert SQL developer" in prompt
