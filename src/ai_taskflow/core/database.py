"""Database configuration and session management for async SQLAlchemy."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.ai_taskflow.core.config import settings

# 1. Create the async connection engine (connection pool).
# echo=True makes SQLAlchemy print all generated SQL to console (great for debugging).
async_engine = create_async_engine(
    settings.db.async_url,
    echo=settings.ENVIRONMENT == "development",
    future=True,
)

# 2. Configure the session factory (factory for our DbContext equivalent).
# expire_on_commit=False prevents SQLAlchemy from expiring object data after commit,
# avoiding unnecessary queries (unwanted lazy loading) in async scope.
async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# 3. Create the declarative base class that all domain entities will inherit from.
class Base(DeclarativeBase):
    """Base declarative class for ORM mapping."""

    pass


# 4. Dependency/context manager for FastAPI dependency injection.
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Generate an async database session for each HTTP request (scoped session).

    Ensures that the session is closed correctly after the request lifecycle ends,
    even if exceptions occur.

    Yields:
        AsyncSession: An active async database session.
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
