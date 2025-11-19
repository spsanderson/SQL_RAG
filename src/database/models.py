"""
Database Models
"""
from dataclasses import dataclass
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class DatabaseConfig(BaseModel):
    """
    Configuration for database connection.
    """
    host: str = Field(..., description="Database host address")
    port: int = Field(1433, description="Database port")
    database: str = Field(..., description="Database name")
    username: str = Field(..., description="Database username")
    password: str = Field(..., description="Database password")
    driver: str = Field("ODBC Driver 17 for SQL Server", description="ODBC driver name")
    
    # Connection pool settings
    pool_size: int = Field(5, description="Minimum pool size")
    max_overflow: int = Field(10, description="Maximum overflow connections")
    pool_timeout: int = Field(30, description="Pool timeout in seconds")
    pool_recycle: int = Field(3600, description="Pool recycle time in seconds")

@dataclass
class QueryResult:
    """
    Result of a database query.
    """
    columns: List[str]
    rows: List[Dict[str, Any]]
    row_count: int
    execution_time: float
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class SchemaElement:
    """
    Represents a database schema element (table, column, etc.).
    """
    name: str
    type: str  # 'table', 'view', 'column'
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
