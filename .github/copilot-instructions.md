# GitHub Copilot Instructions – AI Taskflow

## Project Overview

AI Taskflow is a study-focused proof-of-concept Python backend.
It demonstrates modern async API architecture, event-driven workflows, AI integrations, and quality tooling.
All suggestions should follow production-style patterns even though this is a PoC.

## Language and Style

- All code, comments, docstrings, variable names, and commit messages must be in English.
- Python 3.14+ syntax and features only.
- Use `async`/`await` for all I/O-bound code (database, HTTP, messaging).
- Apply type annotations to every function signature and class attribute.
- Prefer explicit over implicit. Avoid magic or overly clever code.

## Project Stack

- **Web framework**: FastAPI with Uvicorn (ASGI).
- **ORM**: SQLAlchemy 2.x async API with `AsyncSession` and `AsyncEngine`.
- **Database driver (runtime)**: `asyncpg` — use `postgresql+asyncpg://` connection strings.
- **Database driver (migrations only)**: `psycopg2-binary` — used by Alembic CLI only, never in async code.
- **Migrations**: Alembic.
- **Settings**: `pydantic-settings` — all config loaded from environment variables via a typed `Settings` class.
- **Validation and schemas**: Pydantic v2 models for request/response contracts and structured AI outputs.
- **Auth**: PyJWT for token generation and validation.
- **Cache / rate limiting**: Redis.
- **Messaging**: Google Cloud Pub/Sub (local emulator for development).
- **AI orchestration**: LangChain with `langchain-openai` and `langchain-anthropic`.
- **HTTP client (sync flows only)**: Requests.
- **Containerization**: Docker and Docker Compose.

## Package and Dependency Management

- Use Poetry for all dependency and environment management.
- Never edit `poetry.lock` manually.
- Add runtime deps with `poetry add <package>`.
- Add dev deps with `poetry add --group dev <package>`.
- Run project commands via `poetry run <cmd>` (equivalent to `npm run` in Node).
- Use `./scripts/helper.sh` for a menu of common commands.

## Project Layout

Source code lives under `src/ai_taskflow/`. The main modules are:

- `src/ai_taskflow/core/config.py` — typed settings via `pydantic-settings`.
- `src/ai_taskflow/core/database.py` — async SQLAlchemy engine and session factory.
- `src/ai_taskflow/core/security.py` — JWT helpers.
- `src/ai_taskflow/models/` — SQLAlchemy ORM models.
- `src/ai_taskflow/schemas/` — Pydantic request/response and AI output schemas.
- `src/ai_taskflow/api/deps.py` — FastAPI dependency injection helpers.
- `src/ai_taskflow/api/v1/` — versioned API endpoints (`auth.py`, `tasks.py`, `maintenance.py`).
- `src/ai_taskflow/services/cache.py` — Redis-backed caching and rate limiting.
- `src/ai_taskflow/services/publisher.py` — Pub/Sub event publishing.
- `src/ai_taskflow/worker/` — background async task worker and LangChain AI engine.
- `tests/` — pytest test files with `conftest.py` and `pytest-asyncio` fixtures.

## Code Patterns to Follow

- Load all configuration through `src/ai_taskflow/core/config.py` using `pydantic-settings`. Never hardcode credentials or URLs.
- Use SQLAlchemy `AsyncSession` with `async with` context managers. Never use sync sessions in async code.
- Define Pydantic models for every API request body, response, and structured AI output.
- Use FastAPI dependency injection (`Depends`) for database sessions, auth, and rate limiting.
- Use `pytest-asyncio` for all async tests. Mark async tests with `@pytest.mark.asyncio`.
- Prefer `asyncpg` for any runtime database interaction; use `psycopg2-binary` only in Alembic migration scripts.

## Quality Tools

- **Ruff**: linting and formatting — `poetry run ruff check src/` and `poetry run ruff format src/`.
- **MyPy**: strict type checking — `poetry run mypy src/`.
- **Pre-commit**: runs Ruff and MyPy before every commit — `poetry run pre-commit run --all-files`.
- **Pytest**: `poetry run pytest`.

All suggestions must pass Ruff and MyPy checks without errors.

## Architecture Flow

```
Client Request
  → FastAPI (auth, validation, rate limit)
  → SQLAlchemy Async (PostgreSQL via asyncpg)
  → Pub/Sub Publisher (GCP or emulator)
    → Async Worker
      → LangChain (OpenAI or Claude)
      → SQLAlchemy Async (save result)
```

## What to Avoid

- Do not use synchronous database drivers (`psycopg2`) in FastAPI or worker code.
- Do not use `time.sleep` — prefer `asyncio.sleep`.
- Do not hardcode secrets, passwords, or API keys anywhere in the code.
- Do not skip type annotations on new functions or class attributes.
- Do not use `Any` unless absolutely necessary and justified with a comment.
- Do not generate code that bypasses the pre-commit hooks or quality checks.
