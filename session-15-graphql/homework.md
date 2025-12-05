# Python Interview Questions & Coding Challenges - Session 15

## Concept Questions

- What is GraphQL and how does it differ from REST? What problems does it solve?
  - Key differences from REST:
    - Single endpoint vs multiple:
      - REST: many endpoints (/users/1, /users/1/posts, etc.)
      - GraphQL: usually one endpoint (/graphql) and the client specifies the shape of the data in the query.
    - Client-controlled vs server-controlled shape:
      - REST: server decides the response structure.
      - GraphQL: client asks for specific fields and nesting.
    - Over-fetching / under-fetching:
      - REST often returns too much data (over-fetch) or not enough (under-fetch, requiring multiple calls).
      - GraphQL solves this by allowing precise selection of fields.
    - Multiple round trips vs single request:
      - REST: may need several requests to aggregate data from different resources.
      - GraphQL: can fetch all related data in one request (user + posts + comments).
    - Problems it solves:
      - Over-fetching and under-fetching of data.
      - Multiple round-trips to build a complex UI.
      - Tight coupling between front-end and back-end response formats.
      - Difficult evolution of APIs (clients can just request new fields when added).

- What is the N+1 query problem in GraphQL and how can it be resolved?
  - N+1 problem:
    - In GraphQL, resolvers are field-based and often executed per item.
    - Example: You query users { id name posts { id title } }.
      - Resolver for users runs 1 DB query to get N users.
      - For each user, the posts resolver runs a new DB query.
      - Total = 1 (for users) + N (for posts) = N+1 queries, which is very inefficient.
    - How to resolve:
      - Use batching and caching, typically via DataLoader pattern.
      - Instead of querying posts per user, collect all user IDs from the field resolvers, then run one query like SELECT * FROM posts WHERE user_id IN (...) and map results back to each user.
      - This reduces N+1 to 2 queries (one for users, one for all posts).

- Describe the difference between nullable and non-nullable fields in GraphQL. How do you denote them in the schema?
  - Nullable field: no ! ex: id: ID
  - Non-nullable field: yes ! ex: id: ID!
  
- What is the DataLoader pattern and why is it important for GraphQL performance?
  - What it does:
    - Collects all load requests for a certain key type during a tick of the event loop.
    - Issues one batched call instead of many.
    - Caches results so if the same key is requested again in the same request, it doesn’t hit the DB again.
  - Why it’s important in GraphQL:
    - GraphQL resolvers are often called per field, per object, which easily creates the N+1 query problem.
    - DataLoader lets you:
      - Batch those field-level calls into one DB query.
      - Cache results within a single GraphQL request.
      - Result: huge performance improvement and fewer DB round-trips.

- What are GraphQL fragments and when would you use them?
  - Fragments let you define a reusable selection of fields and then spread it into multiple queries.
  - When to use:
    - When multiple queries or multiple parts of a query need the same field selection.
    - To simplify refactoring — you change the fragment once, not many queries.

- How would you implement pagination in a Python GraphQL API?
  - In a Python GraphQL API, I usually implement pagination in one of two ways. For simple cases, I use offset-based pagination, where the query accepts offset and limit and the resolver simply applies those to the database query. It’s easy and works well for small datasets.
  - For production, I prefer cursor-based pagination. I generate a stable cursor—usually by encoding an ID or timestamp—and when the client requests first: N, after: cursor, the resolver fetches the next slice and returns edges and pageInfo fields. Cursor-based pagination avoids issues like skipping or repeating items when data changes and scales much better for large datasets

- How do you handle errors and exceptions in GraphQL resolvers?
  - GraphQL responses always return:
    - A data field, and optionally
    - An errors array.
  - At resolver level:
    - If a resolver raises an exception:
      - GraphQL will null out that field in data.
      - Add an entry to the errors array with message + path.
    - You can:
      - Raise domain-specific exceptions and map them to user-friendly error messages.
      - Use custom error classes and middleware.
  
## Coding Challenge:
# GraphQL Integration Challenge - Task Management with Weather

## Challenge Overview

Build a GraphQL API server that integrates with your existing FastAPI REST service (Session 11 homework). Both servers will run simultaneously on different ports, with GraphQL acting as a gateway that communicates with the FastAPI backend.

## Setup

- **FastAPI REST Server**: Run on `http://localhost:8000`
- **GraphQL Server**: Run on `http://localhost:8001`

```bash
fastapi dev main.py --port=8001
```

## Requirements

### 1. GraphQL Schema

Define types for:
```graphql
type User {
  id: ID!
  name: String!
  tasks: [TaskListItem!]!
}

type TaskListItem {
  id: ID!
  title: String!
  content: String!
  city: String!
  userId: ID!
}

type Task {
  id: ID!
  title: String!
  content: String!
  city: String!
  userId: ID!
  user: User!
  weather: Weather!
}

type Weather {
  temperature: Float!
  windspeed: Float!
  weathercode: Int!
  time: String!
}
```

**Important:** `TaskListItem` does NOT include weather. Only the single `Task` query returns weather data.

### 2. Queries to Implement

```graphql
type Query {
  # Get all users
  users: [User!]!
  
  # Get single user with their tasks (no weather)
  user(id: ID!): User
  
  # Get all tasks with optional filters (no weather)
  tasks(userId: ID, city: String): [TaskListItem!]!
  
  # Get single task WITH weather forecast
  task(id: ID!): Task
}
```

### 3. Mutations to Implement

```graphql
type Mutation {
  # User operations
  createUser(name: String!): User!
  deleteUser(id: ID!): User!
  
  # Task operations
  createTask(title: String!, content: String!, city: String!, userId: ID!): Task!
  updateTask(id: ID!, title: String, content: String, city: String): Task!
  deleteTask(id: ID!): Task!
}
```

**Note:** Mutations return `Task` type (with weather) for single task operations.

### 4. Integration Requirements

Your GraphQL resolvers should:
- Make HTTP requests to FastAPI endpoints using `httpx`
- Handle async/await for all external API calls
- Map REST responses to GraphQL types
- Pass through query parameters for filtering
- **Only fetch weather when querying a single task**


### 5. Solve the N+1 Problem

When fetching `users` with their `tasks`, implement DataLoader or batch requests to avoid N+1 queries to the FastAPI server.

**Example scenario:**
```graphql
query {
  users {
    name
    tasks {
      title
      city
    }
  }
}
```

If you have 10 users, this should make **2 requests** (1 for users, 1 batched for all tasks), not 11 requests.