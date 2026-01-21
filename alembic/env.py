# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ══════════════════════════════════════════════════════════════════
# IMPORTANTE: Importe sua Base e TODAS as entidades
# ══════════════════════════════════════════════════════════════════
from infra.configs.database import Base

# Importar todas as entidades para que Alembic as "veja"
from infra.entities.team import Team
from infra.entities.user import User
from infra.entities.report import Report
from infra.entities.project import Project
from infra.entities.ticket import Ticket
from infra.entities.form import Form
from infra.entities.chat import Chat
from infra.entities.message import Message
from infra.entities.associations import *  # Todas as tabelas de associação

# Configuração do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Roda migrations em modo 'offline' (gera SQL sem conectar)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Roda migrations em modo 'online' (conecta ao banco)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()