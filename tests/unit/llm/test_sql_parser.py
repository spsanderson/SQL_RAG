"""
Test SQL Parser
"""
import pytest
from src.llm.sql_parser import SQLParser

def test_parse_extracts_sql_block():
    """
    Test extracting SQL from a markdown code block.
    """
    parser = SQLParser()
    response = """
Here is the query:
```sql
SELECT * FROM users
```
Hope that helps!
"""
    sql = parser.parse(response)
    assert sql == "SELECT * FROM users"

def test_parse_extracts_generic_block():
    """
    Test extracting SQL from a generic code block.
    """
    parser = SQLParser()
    response = """
```
SELECT * FROM users
```
"""
    sql = parser.parse(response)
    assert sql == "SELECT * FROM users"

def test_parse_extracts_raw_text():
    """
    Test extracting SQL from raw text.
    """
    parser = SQLParser()
    response = "SELECT * FROM users"
    sql = parser.parse(response)
    assert sql == "SELECT * FROM users"

def test_parse_removes_prefix():
    """
    Test removing 'SQL Query:' prefix.
    """
    parser = SQLParser()
    response = "SQL Query: SELECT * FROM users"
    sql = parser.parse(response)
    assert sql == "SELECT * FROM users"
