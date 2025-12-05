# Python Interview Questions & Coding Challenges - Session 15

## Concept Questions

- What's the difference between unit tests, integration tests, and end-to-end tests? When would you use each?
  - Unit tests:
    - Test a single function or module in isolation.
    - Fast, precise, catch small logic bugs.
    - Use heavy mocking
    - Use when: validating core logic and edge cases.
  - Integration tests:
    - Test how multiple components work together (e.g., DB + API layer).
    - Slower but ensure boundaries are correct
    - Use when: verifying interactions, contracts, and real workflows.
  - End-to-end (E2E) tests:
    - Test the whole system from the user’s perspective, usually through the UI or API.
    - Slowest but highest confidence
    - Use when: validating full business flows.

- Explain the purpose of mocking in unit tests. What's the difference between Mock, MagicMock, and patch in Python's unittest.mock?
  - Purpose of mocking:
    - Replace real dependencies (DB, network, external services) with lightweight, predictable substitutes so unit tests stay fast and isolated.
  - Mock:
    - Basic fake object that can record calls and return values.
  - MagicMock:
    - Same as Mock but includes Python “magic methods” (like __len__, __getitem__, iteration, arithmetic support).
    - Useful when the object needs to behave like a container or number.
  - patch:
    - Temporarily replaces a real object (e.g., function, class, environment variable) with a Mock during a test.
    - Can be used as a decorator or context manager.

- Explain test coverage. What's a good coverage percentage to aim for?
  - Test coverage:
    - A metric that shows what percentage of your code executes during tests.
    - Types include line, branch, and function coverage.
  - Ideal coverage:
    - Usually 80–90%.
    - 100% isn't required — some code is not worth testing (logging, defensive checks).
    - More important than the number is testing the critical logic paths thoroughly.

- How do you handle testing code that involves database operations? What strategies can you use to avoid hitting real databases?
  - Strategies to avoid hitting real databases:
    - Use an in-memory database
    - Use a test database with transactions
    - Mock the database layer
    - Use fixtures for setup/teardown
  - Rule of thumb:
    - Unit tests → mock DB.
    - Integration tests → use real or test DB.

- What's test-driven development (TDD)?
  - TDD is a development workflow consisting of three steps:
    - Write a failing test (define the expected behavior).
    - Write the minimal code to make the test pass.
    - Refactor code while keeping tests green.

- Explain the typical stages in a CI/CD pipeline. What happens in each stage?
  - “A CI/CD pipeline automates the entire lifecycle of building, testing, and deploying software. It generally follows this sequence:
    - Plan – Teams organize work using tools like Jira or Confluence. Requirements, tasks, and sprint goals are defined.
    - Code – Developers write code in version control systems like GitHub or GitLab. Pull requests, code reviews, and branching strategies happen here.
    - Build (CI begins) – Code is compiled or packaged using tools like Gradle or Webpack. Dependencies are installed and artifacts are created.
    - Test – Automated tests run, such as unit tests (JUnit, Jest) and end-to-end tests (Playwright). The goal is to catch issues early.
    - Release – The pipeline bundles production-ready artifacts and prepares them for deployment. Tools like Jenkins or Buildkite orchestrate this.
    - Deploy (CD begins) – The application is deployed to staging or production using tools like Docker, ArgoCD, Kubernetes, or Terraform. This step may include blue-green or canary releases.
    - Operate – The deployed system runs in its target environment. Infrastructure orchestration and autoscaling happen here.
    - Monitor – Tools like Prometheus or Datadog track application metrics, logs, errors, performance, and alerting. Observability ensures fast detection and rollback of issues.
  - The loop continues continually. CI focuses on integrating and testing code frequently, while CD ensures that deployments are consistent, automated, and reliable

- What's the purpose of environment variables and secrets management in CI/CD? How do you handle sensitive data?
  - Environment variables allow configuration to change per environment (dev/staging/prod) without modifying code.
  - Secrets management ensures sensitive values are securely stored.
    - API keys
    - DB passwords
    - Private tokens
    - Credentials
  - Best practices:
    - Never hardcode secrets
    - Store them in a secrets manager (AWS Secrets Manager, Vault, GitHub Actions Secrets)
    - Inject them as environment variables at runtime
    - Grant only minimal required permissions

- Explain the roles in Scrum: Product Owner, Scrum Master, and Development Team. What are each person's responsibilities?
  - Product Owner
    - Owns product vision and priorities.
    - Maintains the backlog, defines user stories, accepts/rejects work.
    - Maximizes value delivered.
  - Scrum Master
    - Facilitates the Scrum process.
    - Removes blockers, coaches the team, ensures ceremonies run smoothly.
    - Not a manager — a servant leader.
  - Development Team
    - Cross-functional engineers who build the product.
    - Self-organizing, responsible for delivering increments each sprint.
    - Estimate work, commit to sprint goals, collaborate daily.

## Coding Challenge:
## Challenge: Unit Testing, CI/CD, and Deployment for FastAPI Note App

**Description:**

Extend the built the FastAPI "note app" in a previous assignment (see session-11-fast-api-2) with automated unit tests, configure a CI workflow with GitHub Actions, and deploy your app to a public service.

### Requirements

1. **Unit Tests**
    - Write unit tests that cover at least the following:
        - Models: Test creation of `User` and `Note` objects and their relationships.
        - API Endpoints: Test the main CRUD routes (create, read, update, delete notes).
        - Edge Cases: Try invalid input and assert error handling (e.g., duplicate users, unauthorized access).
    - Use `pytest` as your testing framework.
    - Aim for at least **80% code coverage**. Check coverage with `pytest-cov`.

2. **CI with GitHub Actions**
    - Create a `.github/workflows/ci.yaml` workflow file that does the following on every push and pull request:
        - Set up Python.
        - Install dependencies.
        - Run the tests and report coverage.
    - Ensure the workflow fails if tests fail or if coverage drops below your threshold.

3. **Deployment**
    - Deploy your FastAPI app to a public PaaS of your choice. You may use:
        - **Railway** (https://railway.app)
        - **Render** (https://render.com)
        - **Fly.io** (https://fly.io)
        - Or similar free service.
    - The service must be accessible via a public HTTP endpoint.
    - Use secrets for database credentials/API keys in your CI workflow.
