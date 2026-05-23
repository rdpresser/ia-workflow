import sys
from logging.config import fileConfig
from os import path

from alembic import context
from sqlalchemy import engine_from_config, pool

# 1. Ajuste do Path para o Python achar nossa pasta src-layout
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), "../")))

# Importamos nossas configurações e a Base do SQLAlchemy
from src.ai_taskflow.core.config import settings
from src.ai_taskflow.core.database import Base

# IMPORTANTE: Importe o modelo para que os metadados registrem a tabela 'tasks'

# Configura o logger do Alembic baseado no alembic.ini
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Informa os metadados das nossas entidades de domínio para o Autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Roda migrações em modo 'Offline' (Gera scripts SQL puros)."""
    url = settings.db.sync_url  # Usa a URL síncrona do nosso config.py
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Roda migrações em modo 'Online' (Aplica diretamente no banco de dados)."""
    # Sobrescreve dinamicamente a URL de conexão do alembic.ini pela nossa do config.py
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
