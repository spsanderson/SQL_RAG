"""
Custom Exception Classes for the SQL RAG Application.

This module defines a hierarchy of exceptions used throughout the application
for error handling and flow control.
"""


class SQLRAGException(Exception):
    """Base exception for the SQL RAG application."""


class ConfigurationError(SQLRAGException):
    """Raised when there is a configuration error."""


class DatabaseError(SQLRAGException):
    """Raised when a database operation fails."""


class LLMGenerationError(SQLRAGException):
    """Raised when LLM generation fails."""


class SecurityError(SQLRAGException):
    """Raised when a security violation is detected."""


class ValidationError(SQLRAGException):
    """Raised when input validation fails."""
