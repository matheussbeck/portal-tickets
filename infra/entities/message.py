from sqlalchemy import ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from infra.configs.database import Base


class Message(Base):
    """
    Mensagem dentro de um chat de ticket.

    Relacionamentos:
    - N-1: chat (Chat) - mensagem pertence a um chat
    - N-1: user (User) - mensagem foi enviada por um usuário
    """
    __tablename__ = "messages"

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    message_chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False
    )
    message_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    # =========================================================================
    # CONTEÚDO
    # =========================================================================
    message_content: Mapped[str] = mapped_column(String, nullable=False)
    message_type: Mapped[str] = mapped_column(String, default="text")  # text, file, system, status_change
    message_attachments: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        init=False
    )  # JSON array de arquivos

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    message_is_internal: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )  # mensagem interna (não visível para cliente)

    # =========================================================================
    # DATAS
    # =========================================================================
    message_edited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False
    )

    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================

    # N - 1 (Mensagem pertence a um Chat e foi enviada por um User)
    chat: Mapped["Chat"] = relationship(
        back_populates="messages",
        lazy="raise",
        init=False
    )
    user: Mapped["User"] = relationship(
        lazy="raise",
        init=False
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'message_chat_id': self.message_chat_id,
            'message_user_id': self.message_user_id,
            'message_content': self.message_content,
            'message_type': self.message_type,
            'message_attachments': self.message_attachments,
            'message_is_internal': self.message_is_internal,
            'message_edited_at': self.message_edited_at.isoformat() if self.message_edited_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'deleted_by': self.deleted_by,
            'active': self.active.value if self.active else None
        }

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, message_chat_id={self.message_chat_id}, message_user_id={self.message_user_id})>"
