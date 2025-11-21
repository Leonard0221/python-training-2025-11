# Python Interview Questions & Coding Challenges - Session 9

## Concept Questions

- Difference between authentication and authorization
  - Authentication = “Who are you?” It is the process of verifying identity.
    - Examples:
      - Logging in with username + password
      - Using a fingerprint or face scan
      - Using a token from Google login
  - Authorization = “What can you do?” It is the process of determining what an authenticated user is allowed to access.
    - Examples:
      - Admin vs normal user permissions
      - A user allowed to update only their own posts
      - Access to specific APIs
  - Key idea:
    - You must authenticate before you can be authorized.

- What are HTTP cookies? How do they work and what are their main use cases?
  - Cookies are small pieces of data stored in the browser and sent to the server with each request to the same domain.
  - How they work:
    - Server sends a Set-Cookie header.
    - Browser stores the cookie.
    - Browser automatically attaches the cookie with every request to that server domain.
    - Server reads cookie to identify session/user.
  - Main use cases
    - Session management (most common): login sessions, cart sessions, authenticated user tracking
    - Personalization: language settings, preferences
    - Analytics / tracking: keeping track of user behavior
  
- What are the limitations of cookies
  - Size limit: about 4 KB per cookie
  - Quantity limit: browser limits cookies per domain
  - Security risks:
    - vulnerable to XSS (if not HttpOnly)
    - vulnerable to CSRF (because cookies auto-send)
  - Stored on client-side only: easier for users to modify/delete
  - Must be sent with every request → increases bandwidth
  - Not good for storing sensitive data

- What is JWT and how does it work?
  - JWT = JSON Web Token. It’s a compact, signed token used for stateless authentication.
  - How it works
    - User logs in with username/password.
    - Server generates a JWT and sends it to the client.
    - Client stores it (usually in localStorage or memory).
    - Client sends JWT in the Authorization: Bearer <token> header.
    - Server verifies signature and extracts the user info — no session storage required.
  
- What are the advantages and disadvantages of using JWT compared to traditional session-based authentication?
  - Advantages of JWT
    - Stateless (server does not store sessions)
    - Easy for scaling and microservices
    - Can store more data inside the token
    - Works well across domains/APIs
  - Disadvantages of JWT
    - Cannot be invalidated easily
    - (server has no session table to delete)
    - Long tokens → increase request size
    - If stored in localStorage, may be vulnerable to XSS
    - If long-lived, dangerous when stolen
    - Rotating/refreshing requires more work
  - Sessions Advantages
    - Easy to invalidate (delete server-side session)
    - Simpler and safer for traditional web apps
  - Sessions Disadvantages
    - Server must store sessions → scaling issues
    - Need sticky sessions or shared session store
  
- How do you invalidate or blacklist JWT tokens?
  - JWTs are stateless by design, so invalidation requires extra mechanisms:
  - Common methods
    - Maintain a token blacklist
      - store invalid tokens (or their jti — token id) in a DB
      - check against blacklist on each request
    - Short-lived access tokens + refresh tokens
      - access token expires quickly (like 5–15 minutes)
      - reduces damage from stolen tokens
    - Rotate refresh tokens
      - invalidate the refresh token in DB upon logout
    - Change the server signing key
      - invalidates ALL tokens at once (drastic)
  
- What is password hashing and why is it important?
  - Password hashing = converting a password into a one-way mathematical representation.
  - Why important?
    - Servers never store plain passwords.
    - Even if database is stolen, hashing protects users.
    - Good hashing algorithms are slow and salted → hard to brute-force.
  - Secure password hashing algorithms
    - bcrypt
    - scrypt
    - PBKDF2
    - Argon2 (best modern standard)
  - Hashing is not encryption — encryption is reversible; hashing is not.

- What is the access / refresh token pattern
  - A common authentication strategy using two tokens:
  - Access Token
    - Short-lived (5–15 minutes)
    - Sent with every request
    - Stored in memory
    - Less risk if stolen
  - Refresh Token
    - Long-lived (days or weeks)
    - Stored securely (httpOnly cookie or secure storage)
    - Used only to request a new access token
    - Server keeps refresh tokens in DB → can revoke them anytime
  - Benefits
    - Reduces harm if access token is stolen
    - Allows logout by deleting refresh token
    - Makes JWT safer

- What is the Oauth2 flow
  - OAuth2 is a framework for delegated authorization. It allows a user to give a third-party app limited access to their data without sharing their password.

---

## Coding Challenge:
Add RBAC to Existing Customer & Order API

## Overview
Enhance your existing Customer and Order management API with a Role-Based Access Control (RBAC) system. Users will be assigned roles, and roles will have specific permissions that control access to customer and order operations.

---

## Database Schema Requirements

### 1. Users Table
Create a user model that stores:
- Basic user information (email, password hash, name)
- A **single role** assigned to each user (one-to-many relationship)

### 2. Roles Table
Create a role model that represents business functions:
- Role name
- Role description
- **Multiple permissions** associated with each role (many-to-many relationship)

### 3. Permissions Table
Create a permission model for specific operations:
- Permission name (see required permissions below)
- Permission description

### 4. Role-Permission Association
Create a **many-to-many** relationship between roles and permissions using an association/junction table.

---

## Required Permissions (9 Total)

### Customer Permissions
- `view_customers` - View customers (both list and details)
- `create_customers` - Create new customers
- `update_customers` - Update customer information
- `delete_customers` - Delete customers

### Order Permissions
- `view_orders` - View orders (both list and details)
- `create_orders` - Create new orders
- `update_orders` - Update order information
- `delete_orders` - Delete orders

### User Management Permission
- `manage_users` - Register new users and assign roles

---

## Required Roles with Permission Assignments

### 1. Admin Role
**Description**: Full system access, can manage everything including user registration

**Permissions**:
- `view_customers`
- `create_customers`
- `update_customers`
- `delete_customers`
- `view_orders`
- `create_orders`
- `update_orders`
- `delete_orders`
- `manage_users`

### 2. Sales Role
**Description**: Can manage customers and orders, but cannot delete or manage users

**Permissions**:
- `view_customers`
- `create_customers`
- `update_customers`
- `view_orders`
- `create_orders`
- `update_orders`

### 3. Viewer Role
**Description**: Read-only access to customers and orders

**Permissions**:
- `view_customers`
- `view_orders`

---

## API Endpoints with Required Permissions

### Authentication Endpoints (New Api)
```
POST   /api/login               → Public (no authentication required)
POST   /api/register            → Requires: manage_users (admin only!)
```

### Customer Endpoints
```
GET    /api/customers           → Requires: view_customers
GET    /api/customers/<id>      → Requires: view_customers
POST   /api/customers           → Requires: create_customers
PUT    /api/customers/<id>      → Requires: update_customers
DELETE /api/customers/<id>      → Requires: delete_customers
```

### Order Endpoints
```
GET    /api/orders              → Requires: view_orders
GET    /api/orders/<id>         → Requires: view_orders
POST   /api/orders              → Requires: create_orders
PUT    /api/orders/<id>         → Requires: update_orders
DELETE /api/orders/<id>         → Requires: delete_orders
```


## Implementation Requirements

### Phase 1: Database Setup
1. Create Users, Roles, Permissions, and Role-Permissions tables
2. Establish proper relationships:
   - Users → Roles (many-to-one)
   - Roles ↔ Permissions (many-to-many with junction table)

### Phase 2: Seed Data
Write a seed script that creates:

**Permissions**:
- `view_customers`
- `create_customers`
- `update_customers`
- `delete_customers`
- `view_orders`
- `create_orders`
- `update_orders`
- `delete_orders`
- `manage_users`

**Roles (3 total) with Permission Assignments**:
- **Admin**: All 9 permissions
- **Sales**: 6 permissions (view/create/update for customers and orders)
- **Viewer**: 2 permissions (view customers and orders)

**Initial Admin User** (important!):
- email: admin@example.com
- password: Admin123
- role: Admin

> **Note**: You MUST create at least one admin user in the seed script, otherwise no one can register new users!

### Phase 3: Authentication
1. **Login endpoint** (POST /api/login):
   - Public endpoint (no authentication required)
   - Accepts email and password
   - Returns JWT token on success
   - JWT must include: user_id, email, role_name, and list of permission names

2. **Register endpoint** (POST /api/register):
   - **Protected by `manage_users` permission** (admin only!)
   - Admin must be logged in to create new users
   - Admin specifies which role to assign to new user
   - Validate inputs with Pydantic

### Phase 4: Authorization System
1. Create `@permission_required(permission_name)` decorator
2. Apply permission decorator to ALL customer and order endpoints
3. Apply permission decorator to register endpoint (`manage_users`)
4. Decorator should:
   - Extract JWT from Authorization header
   - Decode JWT and get permissions list
   - Check if required permission is in user's permissions
   - Return 401 if no token, 403 if insufficient permissions

---

## Business Rules

1. **No Self-Registration**: Regular users cannot register themselves - only admins can create accounts
2. **Initial Admin**: Seed script must create at least one admin user
3. **Admin Creates Users**: Admin decides which role to assign when creating new users
4. **Cannot Delete Roles**: The three roles are fixed (Admin, Sales, Viewer)
5. **JWT Contains Permissions**: Include full permission list in JWT to avoid database lookups on every request

---
