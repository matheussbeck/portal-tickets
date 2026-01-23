
from sqlalchemy import Integer, Boolean, DateTime, func, Enum
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum


class Status(PyEnum):
    """
    Status base para soft delete.

    Para uso em todas as entidades:
    - ATIVO: registro ativo e operacional
    - INATIVO: registro desativado (soft delete)

    Entidades específicas (User, Project, etc.) podem ter
    seus próprios enums de status operacional.
    """
    ATIVO = "ativo"
    INATIVO = "inativo"


class Base(MappedAsDataclass, DeclarativeBase):
    """
    Classe base para todas as entidades.

    Campos de auditoria:
    - created_at/by: quando e quem criou
    - updated_at/by: quando e quem atualizou por último
    - deleted_at/by: quando e quem fez soft delete
    - active: status do registro (ATIVO/INATIVO)

    Nota: created_by, updated_by e deleted_by são Integer simples
    (não FKs) para evitar ambiguidade nos relationships com User.
    A integridade é garantida pela aplicação, não pelo banco.
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        init=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False
    )

    # Auditoria de usuários (Integer, não FK para evitar ambiguidade)
    created_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False
    )
    updated_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False
    )
    deleted_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False
    )

    # Soft delete
    active: Mapped[Status] = mapped_column(
        Enum(Status),
        default=Status.ATIVO,
        init=False
    )

    # =========================================================================
    # MÉTODOS
    # =========================================================================

    def to_dict(self) -> dict:
        """
        Converte entidade para dicionário.

        - Converte Enums para seus valores (.value)
        - Converte datetime para ISO format
        - Ignora relationships (apenas colunas)

        Para serialização completa com relacionamentos,
        use os Pydantic Schemas.
        """
        from sqlalchemy import inspect
        from enum import Enum as PyEnum

        result = {}
        mapper = inspect(self.__class__)

        for column in mapper.columns:
            value = getattr(self, column.key)

            # Converter Enums para string
            if isinstance(value, PyEnum):
                value = value.value
            # Converter datetime para ISO
            elif isinstance(value, datetime):
                value = value.isoformat()

            result[column.key] = value

        return result

