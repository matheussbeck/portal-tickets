
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

    IMPORTANTE: Este enum é para soft delete (registro existe ou não).
    Entidades específicas (User, Project, etc.) têm seus próprios
    enums de status OPERACIONAL (ex: UserStatus, ProjectStatus).

    Exemplo:
        - User com active=INATIVO: foi "deletado" do sistema
        - User com active=ATIVO e user_status=FERIAS: existe mas está de férias
    """
    ATIVO = "ativo"
    INATIVO = "inativo"


class Base(MappedAsDataclass, DeclarativeBase):
    """
    Classe base abstrata para todas as entidades do sistema.

    Fornece campos padrão de auditoria herdados automaticamente
    por todas as entidades que herdam de Base.

    Campos Herdados (todos com init=False):
        id: Chave primária autoincrement
        created_at: Data/hora de criação (preenchido pelo banco)
        updated_at: Data/hora da última atualização (auto-update)
        deleted_at: Data/hora do soft delete (None se ativo)
        created_by: ID do usuário que criou (sem FK)
        updated_by: ID do usuário que atualizou (sem FK)
        deleted_by: ID do usuário que deletou (sem FK)
        active: Status de soft delete (ATIVO/INATIVO)

    Por que usar Integer em vez de ForeignKey para *_by:
        Para evitar ambiguidade nos relationships com User.
        Se fossem FKs, cada entidade teria 3 relationships para User
        (created_by, updated_by, deleted_by), conflitando com outros.
        A integridade é garantida pela aplicação, não pelo banco.

    Padrão MappedAsDataclass:
        - Campos com init=False NÃO aparecem no construtor
        - Campos sem init=False SÃO obrigatórios no construtor
        - default/default_factory define valor inicial

    Exemplo de Herança:
        ```python
        class User(Base):
            __tablename__ = "users"

            # Campos específicos do User (obrigatórios no construtor)
            user_full_name: Mapped[str] = mapped_column(String, nullable=False)

            # Campos opcionais (não aparecem no construtor)
            user_photo: Mapped[str | None] = mapped_column(String, init=False)

        # Uso:
        user = User(user_full_name="João")  # id, created_at, etc são automáticos
        ```
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        init=False,
        doc="Chave primária autoincrement"
    )

    # =========================================================================
    # TIMESTAMPS (preenchidos automaticamente pelo banco)
    # =========================================================================
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False,
        doc="Data/hora de criação (server_default=func.now())"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False,
        doc="Data/hora da última atualização (onupdate=func.now())"
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
        doc="Data/hora do soft delete (None enquanto ativo)"
    )

    # =========================================================================
    # AUDITORIA DE USUÁRIOS (Integer, não FK para evitar ambiguidade)
    # =========================================================================
    created_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False,
        doc="ID do User que criou (preenchido pela aplicação)"
    )
    updated_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False,
        doc="ID do User que fez última atualização"
    )
    deleted_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False,
        doc="ID do User que fez soft delete"
    )

    # =========================================================================
    # SOFT DELETE
    # =========================================================================
    active: Mapped[Status] = mapped_column(
        Enum(Status),
        default=Status.ATIVO,
        init=False,
        doc="Status de soft delete: ATIVO (existe) ou INATIVO (deletado)"
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

