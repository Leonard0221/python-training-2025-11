# Python Interview Questions & Coding Challenges - Session 14

## Concept Questions

- Explain the WebSocket protocol and how it differs from HTTP polling and long polling
  - WebSockets provide a full-duplex, persistent connection between client and server. Once the handshake is done, both sides can push data at any time without reopening connections.
  - Differences:
    - HTTP Polling
      - Client repeatedly sends requests like: “Any updates?”
      - Server responds immediately (even if empty).
      - High overhead (many connections, wasted requests).
    - HTTP Long Polling
      - Client sends a request and the server holds it until there is data.
      - After responding, client opens a new request again.
      - Fewer requests than polling, but still not a true persistent connection.
    - WebSockets
      - One connection stays open.
      - Real-time, low-latency, bi-directional.
      - Ideal for chat apps, trading dashboards, multiplayer games.

- What caching strategy would you use for frequently accessed but slowly changing data
  - Best strategy: Read-Through or Cache-Aside with TTL.
    - Data doesn’t change often → caching is safe.
    - Frequently accessed → improves performance a lot.
  - Typical approach:
    - First request: cache miss → load from DB → store in cache.
    - After that: all reads hit cache.
    - Use a TTL (Time-To-Live) to auto-refresh every X minutes.
  - If extremely stable (e.g., country codes, price tiers), you can pre-warm cache on startup.

- Explain the difference between cache-aside, write-through, and write-behind caching patterns
  - Cache-Aside (“Lazy Loading”)
    - App first checks cache → if miss, load from DB → write to cache.
    - Writes: go to DB first, then invalidate/update cache.
    - Pros: Most flexible, avoids stale cache.
    - Cons: First request after expiration is slow.
  - Write-Through
    - Every write goes to cache and DB synchronously.
    - Cache is always fresh.
    - Cons: Slower writes because DB and cache are both updated.
  - Write-Behind (Write-Back)
    - Write goes to cache only.
    - Cache asynchronously flushes to DB later.
    - Pros: Fastest writes, batching to DB.
    - Cons: Risk of data loss if cache crashes.

- Describe the differences between RabbitMQ, Kafka, and SQS in terms of use cases and guarantees
  - RabbitMQ
    - Traditional message broker (AMQP).
    - Good for task queues, worker systems.
    - Messages are pushed to consumers.
    - Flexible routing (topic, fanout, routing keys).
    - At-least-once delivery.
  - Kafka
    - Distributed log system.
    - High throughput, persistent storage.
    - Ideal for event streaming, analytics, real-time pipelines.
    - Consumers pull messages at their own pace.
    - Strong ordering guarantees within a partition.
  - Amazon SQS
    - Fully managed queue service (no servers).
    - Simple, reliable task queue.
    - No message ordering by default (unless FIFO queue).
    - Scales automatically, but limited routing features.
  - Summary:
    - Use RabbitMQ for complex routing or task systems.
    - Use Kafka for high-throughput event streaming.
    - Use SQS for simple, serverless, managed queues.

- What are message queues and why are they important in distributed systems?
  - Message queues allow components to communicate asynchronously by sending messages through a buffer (queue).
  - Why important:
    - Decoupling — producers and consumers don’t need to be online at the same time.
    - Load leveling — queues absorb traffic spikes.
    - Fault tolerance — messages aren’t lost if a service dies.
    - Scalability — you can add more consumers to process work in parallel.
  - Without queues, services become tightly coupled and fragile.

- How would you implement a retry mechanism with exponential backoff for failed message processing?
  - Try to process message.
  - If failure:
    - Wait: base_delay * (2 ** retry_count)
    - Example: 1s → 2s → 4s → 8s → ...
  - Add jitter (random 0–20%) to avoid thundering herd.
  - Limit retries (e.g., max 5 times).
  - If still failing → send to Dead Letter Queue.

- Explain the concept of dead letter queues and when you'd use them
  - A Dead Letter Queue stores messages that cannot be processed successfully.
  - Used when:
    - Message has failed multiple retries.
    - Message format is invalid.
    - Processing timed out.
    - Consumer logic throws unhandled errors.
  - Purpose:
    - Prevent poison messages from blocking the main queue.
    - Allow developers to inspect problematic messages.
    - Improve reliability and system resilience.

- How does FastAPI handle synchronous functions differently?
  - async def endpoints
    - Uses an event loop.
    - Supports concurrency via asyncio.
    - Best for I/O-heavy workloads (API calls, DB queries).
  - normal def endpoints
    - FastAPI runs them in a threadpool using anyio.to_thread.run_sync.
    - Avoids blocking the event loop.
    - Good for CPU-bound or blocking operations.
  - Summary:
    - async def: non-blocking, event-driven.
    - def: executed in threadpool so the event loop remains responsive.

## Coding Question

# Rate Limiter - Interview Challenge

## Stage 1

Design a Rate Limiter that controls the number of requests per user within a time window.

```python

import time
from collections import deque
from typing import Dict 

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.user_requests: Dict[str, deque[float]] = {}
    
    def allow_request(self, user_id: str) -> bool:
        current_time = time.time()
        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque()
        
        request_times = self.user_requests[user_id]
        
        while request_times and request_times[0] <= current_time - self.window_seconds:
            request_times.popleft()
        
        if len(request_times) < self.max_requests:
            request_times.append(current_time)
            return True
        else:
            return False

```

**Example:**
```python
limiter = RateLimiter(max_requests=3, window_seconds=10)

assert limiter.allow_request("alice") == True   # 1st
assert limiter.allow_request("alice") == True   # 2nd
assert limiter.allow_request("alice") == True   # 3rd
assert limiter.allow_request("alice") == False  # 4th - denied

assert limiter.allow_request("bob") == True     # bob's 1st

# After 10 seconds pass, alice's requests expire
```

---


## Stage 2

Optimize your Stage 1 solution to O(1) time complexity using the Token Bucket Algorithm.

**Hint:** Calculate tokens to add based on elapsed time since last refill.

```python
class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float) -> None:
        pass
    
    def allow_request(self, user_id: str) -> bool:
        pass
```

**Example:**
```python
# capacity=5, refill_rate=2 tokens/sec
limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2)

# Use all 5 tokens
assert limiter.allow_request("alice") == True   # token: 4
assert limiter.allow_request("alice") == True   # token: 3
assert limiter.allow_request("alice") == True   # token: 2
assert limiter.allow_request("alice") == True   # token: 1
assert limiter.allow_request("alice") == True   # token: 0
assert limiter.allow_request("alice") == False  # no tokens

# Wait 1 second, gain 2 tokens
# Now alice can make 2 more requests
```


## Token Bucket Algorithm

**Concept:**
Imagine a bucket that:
- Starts with a maximum capacity of tokens (e.g., 5 tokens)
- Tokens refill at a constant rate (e.g., 2 tokens per second)
- Each request consumes 1 token
- If the bucket is empty, the request is denied
- The bucket never overflows (capped at capacity)

**How it works:**
1. User makes a request
2. Calculate how many tokens to add based on elapsed time since last request
3. Add tokens (up to capacity max)
4. If tokens ≥ 1, allow request and consume 1 token
5. If tokens < 1, deny request

**Visual Example:**

```
Time 0s:   Bucket: ●●●●●  (5 tokens, full)
           Request 1: allowed → Bucket: ●●●●  (4 tokens)
           Request 2: allowed → Bucket: ●●●  (3 tokens)
           Request 3: allowed → Bucket: ●●  (2 tokens)
           Request 4: allowed → Bucket: ●  (1 token)
           Request 5: allowed → Bucket: ○  (0 tokens)
           Request 6: DENIED (no tokens)

Time 0.5s: Elapsed: 0.5 seconds × 2 tokens/sec = 1 new token
           Bucket: ●  (1 token)
           Request 7: allowed → Bucket: ○  (0 tokens)

Time 1.0s: Elapsed: 0.5 seconds × 2 tokens/sec = 1 new token
           Bucket: ●  (1 token)
           Request 8: allowed → Bucket: ○  (0 tokens)

Time 1.5s: Elapsed: 0.5 seconds × 2 tokens/sec = 1 new token
           Bucket: ●  (1 token)
           Request 9: allowed → Bucket: ○  (0 tokens)

Time 2.5s: Elapsed: 1 second × 2 tokens/sec = 2 new tokens
           Bucket: ●●  (2 tokens, not capped)
           Request 10: allowed → Bucket: ●  (1 token)
           Request 11: allowed → Bucket: ○  (0 tokens)
```

**Key Points:**
- Token refill is calculated on-demand (no background process)
- Tokens accumulate based on time elapsed since last request
- Bucket capacity caps the maximum tokens
- Allows controlled bursts (use all tokens at once if needed)
- Per-user state: each user has independent tokens and refill time
