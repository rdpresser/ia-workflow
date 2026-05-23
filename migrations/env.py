import sys
from logging.config import fileConfig
from os import path

from alembic import context
from sqlalchemy import engine_from_config, pool

# 1. Add project root to the path so Python can resolve the src-layout package.
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), "../")))

# Import project settings and SQLAlchemy Base metadata.
from src.ai_taskflow.core.config import settings
from src.ai_taskflow.core.database import Base

# IMPORTANT: Import model modules so metadata includes mapped tables.
from src.ai_taskflow.models.task import Task  # noqa: F401

# Configure Alembic logger from alembic.ini.
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Provide metadata for Alembic autogenerate.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode (generate SQL scripts only)."""
    url = settings.db.sync_url  # Use sync URL from project settings.
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode (apply directly to the database)."""
    # Override alembic.ini connection URL with runtime settings.
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = settings.db.sync_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
