"""
Tests for SQLValidator
"""
import pytest
from src.validation.validator import SQLValidator
from src.core.exceptions import SecurityError
from src.database.models import SchemaElement

def test_validator_valid_query():
    validator = SQLValidator()
    query = "SELECT * FROM patients WHERE id = 1"
    assert validator.validate_query(query) is True

def test_validator_prohibited_drop():
    validator = SQLValidator()
    query = "DROP TABLE patients"
    with pytest.raises(SecurityError):
        validator.validate_query(query)

def test_validator_prohibited_delete():
    validator = SQLValidator()
    query = "DELETE FROM patients WHERE id = 1"
    with pytest.raises(SecurityError):
        validator.validate_query(query)

def test_validator_prohibited_update():
    validator = SQLValidator()
    query = "UPDATE patients SET name = 'hacker'"
    with pytest.raises(SecurityError):
        validator.validate_query(query)

def test_validator_case_insensitive():
    validator = SQLValidator()
    query = "drop table patients"
    with pytest.raises(SecurityError):
        validator.validate_query(query)

def test_validator_embedded_keyword():
    validator = SQLValidator()
    # Should allow words that contain keywords but are not keywords themselves
    # e.g. "update_date" column
    query = "SELECT update_date FROM patients"
    assert validator.validate_query(query) is True

def test_validator_empty_query():
    validator = SQLValidator()
    with pytest.raises(SecurityError):
        validator.validate_query("")

def test_validator_schema_validation():
    schema = [
        SchemaElement(name="patients", type="table"),
        SchemaElement(name="visits", type="table")
    ]
    validator = SQLValidator(schema)
    
    # Valid table
    assert validator.validate_schema("SELECT * FROM patients") is True
    
    # Invalid table
    with pytest.raises(SecurityError):
        validator.validate_schema("SELECT * FROM hackers")

def test_validator_complexity():
    validator = SQLValidator()
    
    # Valid complexity
    query = "SELECT * FROM t1 JOIN t2 ON t1.id = t2.id"
    assert validator.validate_complexity(query) is True
    
    # Too many JOINs
    query = "SELECT * FROM t1 JOIN t2 ON x JOIN t3 ON x JOIN t4 ON x JOIN t5 ON x JOIN t6 ON x JOIN t7 ON x"
    with pytest.raises(SecurityError):
        validator.validate_complexity(query)
        
    # Too many SELECTs (subqueries)
    query = "SELECT * FROM (SELECT * FROM (SELECT * FROM (SELECT * FROM t)))"
    with pytest.raises(SecurityError):
        validator.validate_complexity(query)

def test_validator_result_limit():
    validator = SQLValidator()
    
    # Valid limits
    assert validator.enforce_result_limit("SELECT TOP 10 * FROM t") is True
    assert validator.enforce_result_limit("SELECT * FROM t LIMIT 10") is True
    assert validator.enforce_result_limit("SELECT COUNT(*) FROM t") is True
    
    # Missing limit
    with pytest.raises(SecurityError):
        validator.enforce_result_limit("SELECT * FROM t")
