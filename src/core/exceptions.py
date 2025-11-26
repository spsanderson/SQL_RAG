"""
Custom Exception Classes
"""

class SQLRAGException(Exception):
    """Base exception for the SQL RAG application."""
    pass

class ConfigurationError(SQLRAGException):
    """Raised when there is a configuration error."""
    pass

class DatabaseError(SQLRAGException):
    """Raised when a database operation fails."""
    pass

class LLMGenerationError(SQLRAGException):
    """Raised when LLM generation fails."""
    pass

class SecurityError(SQLRAGException):
    """Raised when a security violation is detected."""
    pass

class ValidationError(SQLRAGException):
    """Raised when input validation fails."""
    pass
