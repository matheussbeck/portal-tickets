
from sqlalchemy import Integer, Boolean, DateTime, func, Enum
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum

class Status(PyEnum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"
    BLOQUEADO = "bloqueado"
    EXCLUIDO = "excluido"

class Base (MappedAsDataclass, DeclarativeBase):
    __abstract__ = True

    id : Mapped[int] = mapped_column(Integer,primary_key=True,init=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),init=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),init=False)
    created_by : Mapped[int | None] = mapped_column(Integer, nullable=True, init=False)
    updated_by : Mapped[int | None] = mapped_column(Integer, nullable=True, init=False)
    deleted_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, init=False)
    deleted_by : Mapped[int | None] = mapped_column(Integer, nullable=True, init=False)
    active : Mapped[Status] = mapped_column(Enum(Status), default=Status.ATIVO, init=False)

