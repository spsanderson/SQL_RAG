"""
Pytest Configuration and Fixtures
"""
import pytest
import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture
def mock_env():
    """
    Mock environment variables for testing.
    """
    os.environ['DB_PASSWORD'] = 'test_password'
    yield
    del os.environ['DB_PASSWORD']
