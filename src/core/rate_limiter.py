"""
Rate Limiter Module
"""
import time
import threading
from typing import Optional

class RateLimiter:
    """
    Thread-safe Token Bucket Rate Limiter.
    """
    
    def __init__(self, max_calls: int, period: float):
        """
        Initialize the rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed in the period.
            period: The time period in seconds.
        """
        self.max_calls = max_calls
        self.period = period
        self.tokens = max_calls
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def acquire(self, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        """
        Acquire a token.
        
        Args:
            blocking: If True, block until a token is available.
            timeout: Maximum time to wait if blocking.
            
        Returns:
            True if acquired, False otherwise.
        """
        start_time = time.time()
        
        while True:
            with self.lock:
                self._refill()
                
                if self.tokens >= 1:
                    self.tokens -= 1
                    return True
                
                if not blocking:
                    return False
            
            # Wait a bit before checking again
            # Calculate time to next refill
            time.sleep(0.1)
            
            if timeout and (time.time() - start_time > timeout):
                return False

    def _refill(self):
        """
        Refill tokens based on time elapsed.
        """
        now = time.time()
        elapsed = now - self.last_refill
        
        # Calculate refill amount
        # rate = max_calls / period
        refill_amount = elapsed * (self.max_calls / self.period)
        
        if refill_amount > 0:
            self.tokens = min(self.max_calls, self.tokens + refill_amount)
            self.last_refill = now
