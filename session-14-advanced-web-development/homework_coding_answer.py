# import time
# from collections import deque
# from typing import Dict 

# class RateLimiter:
#     def __init__(self, max_requests: int, window_seconds: int) -> None:
#         self.max_requests = max_requests
#         self.window_seconds = window_seconds
#         self.user_requests: Dict[str, deque[float]] = {}
    
#     def allow_request(self, user_id: str) -> bool:
#         current_time = time.time()
#         if user_id not in self.user_requests:
#             self.user_requests[user_id] = deque()
        
#         request_times = self.user_requests[user_id]
        
#         while request_times and request_times[0] <= current_time - self.window_seconds:
#             request_times.popleft()
        
#         if len(request_times) < self.max_requests:
#             request_times.append(current_time)
#             return True
#         else:
#             return False
        
        
        
# limiter = RateLimiter(max_requests=3, window_seconds=10)

# assert limiter.allow_request("alice") == True   # 1st
# assert limiter.allow_request("alice") == True   # 2nd
# assert limiter.allow_request("alice") == True   # 3rd
# assert limiter.allow_request("alice") == False  # 4th - denied

# assert limiter.allow_request("bob") == True


import time
from typing import Dict, Tuple

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets: Dict[str, Tuple[float, float]] = {}

    def allow_request(self, user_id: str) -> bool:
        now = time.time()
        if user_id not in self.buckets:
            self.buckets[user_id] = (float(self.capacity), now)
        tokens, last_refill = self.buckets[user_id]
        elapsed = now - last_refill
        tokens = min(self.capacity, tokens + elapsed * self.refill_rate)
        last_refill = now
        if tokens >= 1.0:
            tokens -= 1.0
            self.buckets[user_id] = (tokens, last_refill)
            return True
        else:
            self.buckets[user_id] = (tokens, last_refill)
            return False


limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2)

# Use all 5 tokens
assert limiter.allow_request("alice") == True   # token: 4
assert limiter.allow_request("alice") == True   # token: 3
assert limiter.allow_request("alice") == True   # token: 2
assert limiter.allow_request("alice") == True   # token: 1
assert limiter.allow_request("alice") == True   # token: 0
assert limiter.allow_request("alice") == False