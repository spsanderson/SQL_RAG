"""
Tests for Rate Limiter
"""
import time
import pytest
from src.core.rate_limiter import RateLimiter

def test_rate_limiter_allow():
    # Allow 5 calls per 1 second
    limiter = RateLimiter(max_calls=5, period=1.0)
    
    # Should allow 5 immediate calls
    for _ in range(5):
        assert limiter.acquire(blocking=False) is True
        
    # 6th call should fail if non-blocking
    assert limiter.acquire(blocking=False) is False

def test_rate_limiter_refill():
    # Allow 1 call per 0.1 second
    limiter = RateLimiter(max_calls=1, period=0.1)
    
    assert limiter.acquire(blocking=False) is True
    assert limiter.acquire(blocking=False) is False
    
    # Wait for refill
    time.sleep(0.15)
    
    assert limiter.acquire(blocking=False) is True

def test_rate_limiter_blocking():
    # Allow 1 call per 0.1 second
    limiter = RateLimiter(max_calls=1, period=0.1)
    
    assert limiter.acquire(blocking=True) is True
    
    start_time = time.time()
    # This should block for approx 0.1s
    assert limiter.acquire(blocking=True) is True
    duration = time.time() - start_time
    
    assert duration >= 0.09 # Allow some jitter

def test_rate_limiter_timeout():
    # Allow 1 call per 10 seconds (slow)
    limiter = RateLimiter(max_calls=1, period=10.0)
    
    assert limiter.acquire(blocking=True) is True
    
    # Try to acquire another with short timeout
    start_time = time.time()
    assert limiter.acquire(blocking=True, timeout=0.1) is False
    duration = time.time() - start_time
    
    # Should have waited at least timeout
    assert duration >= 0.1
