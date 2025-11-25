# Python Interview Questions & Coding Challenges - Session 10

## Concept Questions

- What's the difference between using requests and httpx for making HTTP calls in FastAPI, and why is httpx preferred in async contexts?
  - requests
    - Purely blocking.
    - Great for simple scripts, but in an async server, calling requests.get() blocks the event loop until the call finishes.
    - In FastAPI async endpoints, using requests defeats the point of async: concurrent requests are stalled while one call waits.
  - httpx
    - Supports both sync and async clients:
    - The async client is fully non-blocking and plays nicely with FastAPI’s event loop.
    - Built-in connection pooling, timeouts, HTTP/2, etc.
  - Why httpx in FastAPI?
    - In async def routes, you can await httpx.AsyncClient calls.
    - This allows true concurrency: while one request waits on I/O, the server can handle others.
    - Using requests inside async def can cause performance issues because it blocks the event loop.

- What are the key differences in the database URL connection string when migrating from sync SQLAlchemy to async SQLAlchemy, and what driver changes are required for PostgreSQL?
  - Sync SQLAlchemy, PostgreSQL:
    - SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:password@host:5432/dbname"
    - from sqlalchemy import create_engine
    - engine = create_engine(SQLALCHEMY_DATABASE_URL)
  - Async SQLAlchemy with PostgreSQL:
    - Use create_async_engine
    - Use an async driver, typically asyncpg (or async psycopg3, but asyncpg is common).
  - Key changes:
    - Prefix driver with +asyncpg instead of +psycopg2.
    - Use AsyncSession and async_sessionmaker.
    - DB operations are now await session.execute(...), await session.commit(), etc.

- What is ASGI (Asynchronous Server Gateway Interface) and how does it differ from WSGI?
  - WSGI – Web Server Gateway Interface
    - Older Python web standard (Flask, Django classic).
    - Designed for synchronous request/response.
    - Each request handled in a thread/process; no native async support.
  - ASGI – Asynchronous Server Gateway Interface
    - Newer standard for async and sync Python web apps (FastAPI, modern Django).
    - Supports long-lived connections (WebSockets, Server-Sent Events) and concurrency with coroutines.
    - Lets frameworks run on async servers such as Uvicorn, Hypercorn, etc.
  - Difference in plain language:
    - WSGI: “one request in, one response out, all blocking”.
    - ASGI: “built for async, can handle HTTP + WebSockets + background tasks, with non-blocking I/O.”

- How is FastAPI different from Flask?
  - FastAPI
    - ASGI-based, designed for async from day one.
    - Heavy use of type hints and Pydantic ⇒ automatic validation and OpenAPI docs.
    - Automatic /docs (Swagger UI) and /redoc docs.
    - Built-in dependency injection system (Depends).
    - Great performance due to Starlette + uvicorn.
  - Flask
    - WSGI-based, primarily synchronous (though extensions exist for async).
    - Micro-framework: minimal core, relies heavily on extensions.
    - No built-in validation or automatic API docs (you add libraries yourself).
    - Routing and request handling are very simple and flexible, great for small apps or when you want to assemble your own stack.
  - Short version: Flask is a lightweight, flexible micro-framework; FastAPI is opinionated, async-ready, and validation-/docs-focused.

- Explain the difference between response_model, response_model_exclude, and response_model_include in FastAPI route decorators. When would you use each?
  - response_model: always, to define the general shape of your response.
  - include: when you want a “summary” version with only a subset (e.g., public profile).
  - exclude: when your model has some sensitive/internal fields you never want to return (passwords, internal IDs).

- How do you implement JWT authentication in FastAPI
  - Install libs: e.g. python-jose (or PyJWT) + passlib for hashing.
  - Create Pydantic models for User, Token, login payload, etc.
  - Password hashing (bcrypt) and user lookup (from DB).
  - Login endpoint to issue JWT
  - OAuth2PasswordBearer dependency
  - Protect routes using the dependency

- How does FastAPI handle synchronous functions differently?
  - synchronous (plain def), FastAPI:
    - Detects it’s not async.
    - Runs the function in a threadpool executor (via AnyIO).
    - This keeps the main event loop free so other async requests can continue.
  - FastAPI offloads sync_route to a worker thread.
    - For async def routes, FastAPI runs them directly on the event loop.


## Coding Challenge:
# Continue - FastAPI Task Management with Weather Forecast

