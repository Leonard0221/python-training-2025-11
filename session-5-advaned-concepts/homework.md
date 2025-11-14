# Python Coding Questions - Session 3: Recursion & Functions

## Concept Questions

- What is a decorator in Python, and where is it used?
  - What: A higher order function that wraps another function to add behavior without changing its code.
  - Where used: Enhancing code reusability. Logging, timing, caching (functools.lru_cache), auth, validation.
  
- What's the difference between a generator and a regular function that returns a list?
  - Generator: uses yield; produces a lazy sequence one item at a time; stateful between yields.
  - List-returning function: builds entire list in memory then returns it.
  - Generators return an iterator; lists are realized containers.
  
- When would you choose generators over lists, and what are the memory implications?
  - Use generators when: Data is large/unknown or streaming. You want constant memory (O(1)) and early consumption.
  - Use when you need random access, len(), multiple passes, or materialize results. O(N)
  
- Explain the difference between threading, multiprocessing, and asyncio in Python
  - Threading: multiple threads within one process; shared memory; good for I/O-bound tasks; affected by GIL (only one thread executes Python bytecode at a time).
  - Multiprocessing: multiple processes with separate memory; bypasses GIL; best for CPU-bound work; higher startup/IPC overhead.
  - Asyncio: single thread, single process, event loop with await on non-blocking I/O; excellent for high-concurrency I/O (sockets, HTTP), not for heavy CPU.
  
- What is the Global Interpreter Lock (GIL)? How does it affect threading and multiprocessing?
  - A mutex in CPython ensuring only one thread executes Python bytecode at a time.
  - Effect:
    - Threading: no speedup for pure CPU-bound Python code; okay for I/O (threads release GIL during blocking I/O or C extensions).
    - Multiprocessing: not affected—each process has its own interpreter and GIL.
  
- When to use threading, asyncio, multiprocess?
  - Threading: Many I/O-bound tasks (web requests, file/network I/O), simpler than asyncio; moderate concurrency (<1k tasks).
  - Asyncio: Massive I/O concurrency (thousands of sockets), cooperative tasks, needs async/await ecosystem.
  - Multiprocessing: CPU-bound workloads (numerical loops, image processing) or when C extensions aren’t used.

- What are CPU-bound vs IO-bound tasks?
  - CPU-bound: time spent computing (e.g., hashing, ML loops). Optimize with algorithms, vectorization, multiprocessing or native code.
  - I/O-bound: time waiting on external resources (disk, network). Optimize with threading/asyncio.

- What's the difference between yield and return in a function?
  - return x: ends function immediately; provides a final value.
  - yield x: pauses function, returns one item, and resumes later; function becomes a generator.
  - A generator can also return (raises StopIteration, optionally with a value accessible via .value in low-level usage).

- What's the difference between using open() with explicit close() vs using the with statement
  - with is better, which automatically closes on success/error; safer; clearer; avoids resource leaks.
  
- How to handle exceptions? Why is exception handling important?
  - try, except SpecificError as e, else, finally
  - Why important: robust error recovery, resource safety, clearer failure semantics, better observability.

---

## Coding Questions
### Coding Problem 1: Decorator

**Problem:**  
Decorator to cache any function return and log hits/misses

**Description:**  
Create a decorator that:
* Caches results for any function with any arguments. (Cache means returning the result directly without calling the function)
* Logs when the function is called
* Logs cache hits
* Logs cache misses

```python
def cache_with_log(func):
    """
    Cache decorator that logs all activity.
    Should work with any function signature.
    """
    cache = {}
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key in cache:
            print(f"[CACHE HIT] {func.__name__} args={args}, kwargs={kwargs}")
            return cache[key]
        else:
            print(f"[CACHE MISS] {func.__name__} args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            cache[key] = result
            return result
    
    return wrapper

# Test cases
@cache_with_log
def add(a, b):
    """Simple function with positional args"""
    return a + b

@cache_with_log
def greet(name, greeting="Hello"):
    """Function with keyword args"""
    return f"{greeting}, {name}!"

@cache_with_log
def calculate(x, y, operation="add"):
    """Function with mixed args"""
    if operation == "add":
        return x + y
    elif operation == "multiply":
        return x * y


# Run tests
print("=== Test 1: Simple function ===")
print(add(2, 3))      # Should log: Cache MISS for args={args}, kwargs={kwargs}
print(add(2, 3))      # Should log: Cache HIT for args={args}, kwargs={kwargs}
print(add(4, 5))      # Should log: Cache MISS for args={args}, kwargs={kwargs}

print("\n=== Test 2: Function with kwargs ===")
print(greet("Alice"))                    # Should log: Cache MISS for args={args}, kwargs={kwargs}
print(greet("Alice"))                    # Should log: Cache HIT for args={args}, kwargs={kwargs}
print(greet("Bob", greeting="Hi"))       # Should log: Cache MISS for args={args}, kwargs={kwargs}
print(greet("Bob", greeting="Hi"))       # Should log: Cache HIT for args={args}, kwargs={kwargs}

print("\n=== Test 3: Mixed args ===")
print(calculate(3, 4))                   # Should log: Cache MISS for args={args}, kwargs={kwargs}
print(calculate(3, 4, operation="add"))  # Should log: Cache HIT for args={args}, kwargs={kwargs}
print(calculate(3, 4, operation="multiply"))  # Should log: Cache MISS for args={args}, kwargs={kwargs}
```


### Coding Problem 2: Batch Generator

**Problem:**  
Create a generator that takes an iterable and yields items in batches of a specified size.

**Description:**  
```python

def batch(iterable, batch_size):
    """
    Generator that yields items in batches.
    
    Args:
        iterable: Any iterable (list, generator, etc.)
        batch_size: Number of items per batch
    
    Yields:
        Lists of items with length = batch_size (last batch may be smaller)
    
    Example:
        >>> list(batch([1, 2, 3, 4, 5, 6, 7], 3))
        [[1, 2, 3], [4, 5, 6], [7]]
        
        >>> list(batch(range(10), 4))
        [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
    """

    current = []
    for i in iterable:
        current.append(i)
        if len(current) == batch_size:
            yield current
            current = []
    if current:
        yield current


# Test cases
print(list(batch([1, 2, 3, 4, 5, 6, 7], 3)))
# [[1, 2, 3], [4, 5, 6], [7]]

print(list(batch(range(10), 4)))
# [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]

print(list(batch("ABCDEFGH", 2)))
# [['A', 'B'], ['C', 'D'], ['E', 'F'], ['G', 'H']]
```

### Coding Problem 3: Async Retry with Exponential Backoff


**Problem**
Create a decorator that retries async functions with exponential backoff.


**Description**
```python
import asyncio
import random

def async_retry(max_attempts=3, base_delay=1, backoff_factor=2):
    """
    Decorator that retries async functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of attempts
        base_delay: Initial delay between retries (seconds)
        backoff_factor: Multiply delay by this factor after each retry
    
    Example:
        @async_retry(max_attempts=3, base_delay=1, backoff_factor=2)
        async def unreliable_function():
            # Will retry with delays: 1s, 2s, 4s
            pass
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    def decorator(func):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("async_retry can only be applied to async functions")

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"[retry] {func.__name__} attempt {attempt}/{max_attempts}")
                    return await func(*args, **kwargs)
                except retry_exceptions as exc:
                    last_exc = exc
                    if attempt == max_attempts:
                        print(f"[retry] {func.__name__} exhausted after {attempt} attempts")
                        raise
                    # exponential backoff: base_delay * backoff_factor^(attempt-1)
                    delay = base_delay * (backoff_factor ** (attempt - 1))
                    if jitter > 0:
                        delay += random.uniform(0, jitter)
                    print(f"[retry] {func.__name__} backoff {delay:.2f}s due to: {exc}")
                    await asyncio.sleep(delay)
            # Should not reach here; raise for safety
            raise last_exc

        return wrapper

    return decorator


# Flaky API simulator
@async_retry(max_attempts=5, base_delay=0.5, backoff_factor=2)
async def flaky_api_call(success_rate=0.3):
    """
    Simulates an unreliable API call.
    
    Args:
        success_rate: Probability of success (0.0 to 1.0)
    """
    print(f"  Attempting API call...")
    await asyncio.sleep(0.1)  # Simulate network delay
    
    if random.random() < success_rate:
        print("Success!")
        return "API response data"
    else:
        print("Failed!")
        raise ConnectionError("API temporarily unavailable")


async def test_retry():
    print("Test 1: Flaky API (30% success rate)")
    try:
        result = await flaky_api_call(success_rate=0.3)
        print(f"Final result: {result}\n")
    except ConnectionError as e:
        print(f"All retries failed: {e}\n")
    
    print("Test 2: Very flaky API (10% success rate)")
    try:
        result = await flaky_api_call(success_rate=0.1)
        print(f"Final result: {result}\n")
    except ConnectionError as e:
        print(f"All retries failed: {e}\n")


asyncio.run(test_retry())
```