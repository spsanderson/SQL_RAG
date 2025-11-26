"""
Tests for SQLValidator
"""
import pytest
from src.validation.validator import SQLValidator
from src.core.exceptions import SecurityError

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
