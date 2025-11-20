# Python Interview Questions & Coding Challenges - Session 8

## Concept Questions

- How does routing work in Flask?
  - In Flask, routing is how we map URLs to Python functions.
  - We define routes using the @app.route() decorator.
  - The string inside route() is the URL pattern.
  - When a request comes in, Flask matches the URL and HTTP method to the first route that fits, and calls that view function.
  
- What is restful service
  - A RESTful service is a web service that follows the principles of REST (Representational State Transfer).
  - Key ideas:
    - Resources: Everything is modeled as a resource (users, posts, orders) with a unique URL.
    - Stateless: Each request contains all information needed; the server doesn’t store client session between requests.
    - HTTP verbs used semantically:
      - GET – read
      - POST – create
      - PUT/PATCH – update
      - DELETE – delete
    - Representations: Data is usually sent as JSON, but could be XML, HTML, etc.
    - Use of HTTP status codes: 200, 201, 404, 400, etc.
  
- What are the categories of HTTP status codes (1xx, 2xx, 3xx, 4xx, 5xx)? Provide examples for each.
  - 1xx – Informational
  - The request was received; the process is continuing.
  - Example: 100 Continue
  
  - 2xx – Success
  - The request was successfully processed.
  - Example: 200 OK, 201 Created
  
  - 3xx – Redirection
  - Client must do something else (usually follow a new URL).
  - Example: 301 Moved Permanently, 302 Found
  
  - 4xx – Client errors
  - Something is wrong with the request.
  - Example: 400 Bad Request, 401 Unauthorized, 404 Not Found
  
  - 5xx – Server errors
  - The server failed to process a valid request.
  - Example: 500 Internal Server Error, 503 Service Unavailable

- What is HTTP and how does it work
  - HTTP (HyperText Transfer Protocol) is the application-level protocol used for communication on the web.
  - High-level flow:
    - Client opens a connection to a server (usually over TCP).
    - Client sends an HTTP request: a start line (method + path + version), headers, and optional body.
    - Server processes the request and runs backend logic.
    - Server sends an HTTP response: status line, headers, and optional body (HTML, JSON, etc.).
    - Connection may close or stay open (keep-alive).
  - It’s stateless: each request is independent; the server doesn’t remember previous requests unless we add sessions/tokens.

- Explain the concept of idempotency in HTTP methods
  - An operation is idempotent if doing it once or many times has the same effect on the server state.
  - Idempotent methods (by design):
    - GET – just reads, no change.
    - PUT – “set this resource to exactly X”; sending the same PUT many times keeps the resource the same.
    - DELETE – deleting the same resource multiple times results in “resource is gone” state.
  - Non-idempotent methods:
    - POST – often used to create new resources; multiple POSTs usually create multiple records, so the effect changes.
  
- Explain the difference between HTTP and HTTPS
  - HTTP: plain text over TCP. Data can be read or modified by anyone who can sniff the traffic.
  - HTTPS: HTTP over TLS/SSL (encrypted tunnel).
    - Provides confidentiality (data is encrypted),
    - integrity (cannot be tampered with easily),
    - and authentication (server presents a certificate to prove its identity).
  
- Design a RESTful API for a blogging platform
  - Basic resources: users, posts, comments.
  - Users
    - POST /users – register a new user
    - GET /users/{id} – get user profile
    - PATCH /users/{id} – update user profile
    - DELETE /users/{id} – delete user (maybe admin only)
  - Posts
    - GET /posts – list posts (with filters: ?author_id=..., ?tag=..., ?page=...)
    - POST /posts – create a new post (title, body, tags)
    - GET /posts/{id} – get a single post
    - PATCH /posts/{id} – edit a post
    - DELETE /posts/{id} – delete a post
  - Comments
    - GET /posts/{post_id}/comments – list comments for a post
    - POST /posts/{post_id}/comments – add a comment
    - DELETE /comments/{id} – delete a comment
  - Other considerations you can mention:
    - Use JSON for request and response bodies.
    - Use proper status codes (201 Created for new post, 404 Not Found, etc.).
    - Authentication: maybe JWT tokens in Authorization: Bearer <token>.
    - Pagination, sorting, error format ({"error": "message"}).
  
- What is the MVC architecture
  - MVC stands for Model–View–Controller. It’s a pattern to separate concerns.
  - Model – represents data and business logic.
        Example: database models, ORM classes (User, Post).
  - View – presentation layer, what the user actually sees.
        Example: HTML templates, JSON responses.
  - Controller – handles incoming requests, uses models to get/update data, then passes data to views.
        Example: route handler functions in Flask or controllers in other frameworks.

- What are Flask's request objects
  - Flask provides a global request object (from flask import request) that represents the incoming HTTP request.
  - 
---

## Coding Challenge:
Create a complete RESTful API for the Customer & Orders model.

```
GET    /api/customers           # Get all customers
GET    /api/customers/<id>      # Get single customer
POST   /api/customers           # Create new customer
PUT    /api/customers/<id>      # Update customer
DELETE /api/customers/<id>      # Delete customer
```

**Customer fields:**
- `id` (Integer, primary key)
- `name` (String, required)
- `email` (String, required, unique)
- `created_at` (DateTime)

```
GET    /api/orders              # Get all orders
GET    /api/orders/<id>         # Get single order
POST   /api/orders              # Create order
PUT    /api/orders/<id>         # Update order
DELETE /api/orders/<id>         # Delete order
```

**Order fields:**
- `id` (Integer, primary key)
- `customer_id` (Integer, foreign key to customers)
- `order_date` (DateTime)
- `total_amount` (Numeric)
- `status` (String, default='pending')

## Requirements
1. Validate required fields
2. Return proper HTTP status codes (200, 201, 404, 400, 500)

---
