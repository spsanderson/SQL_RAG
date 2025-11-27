"""
Tests for SQLValidator.

Tests cover security validation, schema validation, complexity limits,
and JSON schema loading functionality.
"""
import json
import os
import tempfile
import pytest
from src.validation.validator import SQLValidator
from src.core.exceptions import SecurityError
from src.database.models import SchemaElement


def test_validator_valid_query():
    """Test that valid SELECT queries pass validation."""
    validator = SQLValidator()
    query = "SELECT * FROM patients WHERE id = 1"
    assert validator.validate_query(query) is True


def test_validator_prohibited_drop():
    """Test that DROP statements are rejected."""
    validator = SQLValidator()
    query = "DROP TABLE patients"
    with pytest.raises(SecurityError):
        validator.validate_query(query)


def test_validator_prohibited_delete():
    """Test that DELETE statements are rejected."""
    validator = SQLValidator()
    query = "DELETE FROM patients WHERE id = 1"
    with pytest.raises(SecurityError):
        validator.validate_query(query)


def test_validator_prohibited_update():
    """Test that UPDATE statements are rejected."""
    validator = SQLValidator()
    query = "UPDATE patients SET name = 'hacker'"
    with pytest.raises(SecurityError):
        validator.validate_query(query)


def test_validator_case_insensitive():
    """Test that prohibited keyword detection is case-insensitive."""
    validator = SQLValidator()
    query = "drop table patients"
    with pytest.raises(SecurityError):
        validator.validate_query(query)


def test_validator_embedded_keyword():
    """Test that column names containing keywords are allowed."""
    validator = SQLValidator()
    query = "SELECT update_date FROM patients"
    assert validator.validate_query(query) is True


def test_validator_empty_query():
    """Test that empty queries are rejected."""
    validator = SQLValidator()
    with pytest.raises(SecurityError):
        validator.validate_query("")


def test_validator_schema_validation():
    """Test table validation against schema elements."""
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
    """Test query complexity validation."""
    validator = SQLValidator()

    # Valid complexity
    query = "SELECT * FROM t1 JOIN t2 ON t1.id = t2.id"
    assert validator.validate_complexity(query) is True

    # Too many JOINs
    query = (
        "SELECT * FROM t1 JOIN t2 ON x JOIN t3 ON x JOIN t4 ON x "
        "JOIN t5 ON x JOIN t6 ON x JOIN t7 ON x"
    )
    with pytest.raises(SecurityError):
        validator.validate_complexity(query)

    # Too many SELECTs (subqueries)
    query = "SELECT * FROM (SELECT * FROM (SELECT * FROM (SELECT * FROM t)))"
    with pytest.raises(SecurityError):
        validator.validate_complexity(query)


def test_validator_result_limit():
    """Test result limit enforcement."""
    validator = SQLValidator()

    # Valid limits
    assert validator.enforce_result_limit("SELECT TOP 10 * FROM t") is True
    assert validator.enforce_result_limit("SELECT * FROM t LIMIT 10") is True
    assert validator.enforce_result_limit("SELECT COUNT(*) FROM t") is True

    # Missing limit
    with pytest.raises(SecurityError):
        validator.enforce_result_limit("SELECT * FROM t")


def test_validator_json_schema_loading():
    """Test loading schema from JSON file."""
    schema_data = {
        "Patients": {
            "columns": [
                {"name": "PatientID", "type": "INTEGER"},
                {"name": "FirstName", "type": "TEXT"},
                {"name": "LastName", "type": "TEXT"}
            ],
            "foreign_keys": []
        },
        "Visits": {
            "columns": [
                {"name": "VisitID", "type": "INTEGER"},
                {"name": "PatientID", "type": "INTEGER"},
                {"name": "VisitDate", "type": "DATE"}
            ],
            "foreign_keys": []
        }
    }

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False
    ) as f:
        json.dump(schema_data, f)
        temp_path = f.name

    try:
        validator = SQLValidator(schema_json_path=temp_path)

        # Check tables are loaded
        assert "PATIENTS" in validator.table_names
        assert "VISITS" in validator.table_names

        # Check columns are loaded
        assert "PATIENTID" in validator.column_map["PATIENTS"]
        assert "FIRSTNAME" in validator.column_map["PATIENTS"]
        assert "VISITID" in validator.column_map["VISITS"]

        # Valid table
        assert validator.validate_schema("SELECT * FROM Patients") is True

        # Invalid table
        with pytest.raises(SecurityError):
            validator.validate_schema("SELECT * FROM NonExistent")

    finally:
        os.unlink(temp_path)


def test_validator_column_validation():
    """Test column validation against schema."""
    schema = [
        SchemaElement(name="patients", type="table"),
        SchemaElement(
            name="patients.id",
            type="column",
            metadata={"table": "patients", "dtype": "INTEGER"}
        ),
        SchemaElement(
            name="patients.name",
            type="column",
            metadata={"table": "patients", "dtype": "TEXT"}
        )
    ]
    validator = SQLValidator(schema)

    # Valid column reference
    assert validator.validate_columns(
        "SELECT patients.id, patients.name FROM patients"
    ) is True

    # Invalid column reference
    with pytest.raises(SecurityError):
        validator.validate_columns("SELECT patients.nonexistent FROM patients")


def test_validator_json_schema_invalid_file():
    """Test that invalid JSON schema file raises SecurityError."""
    with pytest.raises(SecurityError):
        SQLValidator(schema_json_path="/nonexistent/path/schema.json")
