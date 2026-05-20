# AI Taskflow

AI Taskflow is a study-focused Python model project.
It is a PoC used to learn modern API architecture, async workflows, quality tooling, and cloud/event integrations.

## Main Tech Stack

- FastAPI: Async web framework used to build REST APIs with automatic OpenAPI docs.
- Uvicorn: ASGI server that runs the FastAPI application.
- Pydantic and pydantic-settings: Typed validation models and environment-based application settings.
- SQLAlchemy: ORM and SQL toolkit for database modeling and data access.
- Alembic: Database migration tool for SQLAlchemy models.
- psycopg2-binary: PostgreSQL driver used for synchronous tooling such as Alembic CLI migrations.
- asyncpg: Async PostgreSQL driver used by SQLAlchemy Async in the FastAPI runtime.
- Redis: In-memory data store for caching, fast lookups, and temporary state.
- PyJWT: JWT encode/decode library for auth token workflows.
- Requests: HTTP client for calling external APIs in sync flows.
- Google Cloud Scheduler: Managed cron-like scheduler to trigger jobs on a schedule.
- Google Cloud Pub/Sub: Managed messaging service for event-driven communication.
- LangChain: Core orchestration library for LLM-based workflows, including structured outputs.
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

## Common Poetry Commands

Below are the most useful Poetry commands for managing dependencies and the project environment:

```bash
# Lock dependencies (resolve and freeze compatible versions)
poetry lock

# Install all dependencies from lock file and set up the virtualenv
poetry install

# Check for errors or inconsistencies in pyproject.toml
poetry check

# Add a new package (e.g. requests) to your project
poetry add requests

# Add a dev-only package (e.g. pytest) to the [dev] group
poetry add --group dev pytest

# Update all dependencies to the latest compatible versions (according to version constraints)
poetry update

# Update a specific package (e.g. fastapi) to the latest compatible version
poetry update fastapi

# Remove a package from the project
poetry remove requests

# List all installed packages and their versions
poetry show
```


## Helper Script for Common Commands

To use the helper script for common project commands:


1. Make the script executable (run this in the project root):

	chmod +x scripts/helper.sh

2. Run the script:

	./scripts/helper.sh

This script provides a menu to run Poetry commands for installing dependencies, running tests, linting, type checking, and more.
You can also run custom commands using the menu option.
If you see `Permission denied`, ensure you have set the executable permission as above.

Each command should be run from the project root. For more, see the [Poetry documentation](https://python-poetry.org/docs/).
