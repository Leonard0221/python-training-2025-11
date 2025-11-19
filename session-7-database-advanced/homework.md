# Python Interview Questions & Coding Challenges - Session 7

## Concept Questions

- What's the difference between a view, materialized view, and a table? When would you use each?
  - Table: Physically stores data on disk, and data is persistent and updated directly.
  - View: A virtual table created from a SELECT query. It does not store data; it reads from underlying tables every time you query it. Always shows the latest data.
  - Materialized View: Stores the query result physically (like a cached snapshot). Needs to be refreshed manually or on a schedule. Faster for repeated analytical queries.
  - When to use each:
    - Table: Store real business data.
    - View: Security, abstraction, simplify complex queries, always fresh data.
    - Materialized view: Fast read performance for heavy analytical queries where real-time freshness is not critical.
  
- What is ORM? Why do we need ORM?
  - ORM (Object-Relational Mapping) is a technique/tool that maps database tables to classes and rows to objects.
  - Why we need itAvoid writing raw SQL repeatedly：
    - Automatically handle CRUD operations
    - Prevent SQL injection
    - Keep logic in one language (Python, Java, etc.)
    - Improve maintainability
    - Abstract away database differences
  
- Explain the ACID properties. How do they ensure database reliability?
  - ACID ensures reliable database transactions:
    - Atomicity – All steps in a transaction succeed or all fail (no partial writes).
    - Consistency – A transaction brings the database from one valid state to another.
    - Isolation – Transactions don’t interfere with each other; intermediate states are hidden.
    - Durability – Once committed, data will survive crashes or power loss.
  
- Explain the CAP theorem.
  - In a distributed system, you can only guarantee two out of three:
  - C – Consistency: All nodes see the same data at the same time.
  - A – Availability: Every request receives a response.
  - P – Partition Tolerance: System continues to run even if network failures split the nodes.
  
- When would you choose SQL over NoSQL and vice versa?
  - Choose SQL when:
    - Data is structured and relational
    - You need ACID guarantees
    - You need joins, constraints, transactions
    - Data relationships matter (banking, ERP, inventory)
  - Choose NoSQL when:
    - Data is unstructured or semi-structured
    - You need extreme scalability or high availability
    - Large-scale, distributed workloads
    - Flexible schemas (JSON style)
  
- What is eventual consistency?
  - A consistency model where:
    - Updates don’t become visible immediately on all nodes
    - But given enough time, all replicas will converge to the same value
  - Used in distributed systems prioritizing availability over strict consistency (e.g., DNS, Amazon Dynamo, Cassandra).

- What are the different consistency models in distributed systems (strong, weak, eventual)?
  - Strong consistency: Every read returns the most recent write. Behaves like a single machine.
  - Weak consistency: No guarantee that reads return the latest value. Behavior depends on timing.
  - Eventual consistency: Weak consistency + guarantee that data will eventually converge.
  
- Explain the difference between horizontal scaling (scaling out) and vertical scaling (scaling up).
  - Vertical Scaling (Scale Up): Add more power to one machine (more RAM, CPU). Simple but limited.
  - Horizontal Scaling (Scale Out): Add more machines to a cluster. Supports massive traffic and fault tolerance.
  
- How does MongoDB handle transactions and ACID properties?
  - Historically, MongoDB did not support full ACID. But since MongoDB 4.0+, it supports multi-document ACID transactions.
    - Atomicity: Transactions or single-document writes are atomic
    - Consistency: Uses schema validation and distributed guarantees
    - Isolation: Snapshot isolation
    - Durability: Journaling ensures writes survive failures
    - Best used in workloads where data is document-based, but transactional correctness is needed.
  
- What is sharding in databases? How does it differ from partitioning?
  - Sharding
    - Horizontal partitioning of data across multiple servers
    - Each shard holds a subset of the data
    - Used for scalability in distributed systems (MongoDB, Cassandra)
  - Partitioning
    - A more general term that refers to splitting data into smaller pieces
    - Partitions may be on the same machine or multiple machines
    - Can be vertical (columns) or horizontal (rows)
  - Difference
    - Sharding = horizontal partitioning across multiple nodes
    - Partitioning = any logical division of a database (horizontal or vertical, same machine or multiple)
  
---

## Coding Challenge:
The rest part of the Session 6 Library Management System

---
