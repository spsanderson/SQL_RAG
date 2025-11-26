"""
Unit tests for SQLParser.
"""
import pytest
from src.llm.sql_parser import SQLParser

def test_parse_markdown_sql():
    parser = SQLParser()
    response = "Here is the query:\n```sql\nSELECT * FROM table\n```"
    assert parser.parse(response) == "SELECT * FROM table"

def test_parse_markdown_generic():
    parser = SQLParser()
    response = "```\nSELECT * FROM table\n```"
    assert parser.parse(response) == "SELECT * FROM table"

def test_parse_raw():
    parser = SQLParser()
    response = "SELECT * FROM table"
    assert parser.parse(response) == "SELECT * FROM table"

def test_parse_prefix():
    parser = SQLParser()
    response = "SQL Query: SELECT * FROM table"
    assert parser.parse(response) == "SELECT * FROM table"

def test_parse_tags():
    parser = SQLParser()
    response = "<start>SELECT * FROM table<end>"
    assert parser.parse(response) == "SELECT * FROM table"
