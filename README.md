# AI Taskflow

AI Taskflow is a study-focused Python model project.
It is a PoC used to learn modern API architecture, async workflows, quality tooling, and cloud/event integrations.

## Main Tech Stack

- FastAPI: Async web framework used to build REST APIs with automatic OpenAPI docs.
- Uvicorn: ASGI server that runs the FastAPI application.
- SQLAlchemy: ORM and SQL toolkit for database modeling and data access.
- Alembic: Database migration tool for SQLAlchemy models.
- psycopg2-binary: PostgreSQL driver used by SQLAlchemy in sync DB scenarios.
- Redis: In-memory data store for caching, fast lookups, and temporary state.
- PyJWT: JWT encode/decode library for auth token workflows.
- Requests: HTTP client for calling external APIs in sync flows.
- Google Cloud Scheduler: Managed cron-like scheduler to trigger jobs on a schedule.
- Google Cloud Pub/Sub: Managed messaging service for event-driven communication.
- LangChain: Core orchestration library for LLM-based workflows.
- langchain-openai: OpenAI integration package for LangChain.
- langchain-anthropic: Anthropic Claude integration package for LangChain.

## Development and Quality Tools

- Poetry: Dependency and packaging manager for reproducible Python environments.
- Pytest: Testing framework for unit and integration tests.
- pytest-asyncio: Async support for testing coroutine-based code.
- Ruff: Fast linter and formatter for style, quality, and import cleanup.
- MyPy: Static type checker to catch type issues before runtime.
- Pre-commit: Git hook manager that runs checks before each commit.

## Containerization

- Docker: Container runtime to package and run the application consistently.
- Docker Compose: Multi-container orchestration for local environments (for example API + Postgres + Redis).

## Study Plan

See the detailed roadmap and study guide in [STUDY_PLAN.md](STUDY_PLAN.md).
