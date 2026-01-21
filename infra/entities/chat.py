from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.configs.database import Base


class Chat(Base):
    """
    Container de mensagens para um ticket.
    Cada ticket tem exatamente um chat associado.

    Relacionamentos:
    - N-1: ticket (Ticket) - cada chat pertence a um ticket
    - 1-N: messages (Message) - cada chat tem muitas mensagens
    """
    __tablename__ = "chats"

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    chat_ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    # =========================================================================
    # EXTRAS
    # =========================================================================
    chat_title: Mapped[str | None] = mapped_column(String, nullable=True, init=False)

    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================

    # N - 1 (Chat pertence a um Ticket)
    ticket: Mapped["Ticket"] = relationship(
        back_populates="chat",
        lazy="raise",
        init=False
    )

    # 1 - N (Chat tem muitas mensagens)
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        lazy="raise",
        init=False,
        default_factory=list
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'chat_ticket_id': self.chat_ticket_id,
            'chat_title': self.chat_title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'deleted_by': self.deleted_by,
            'active': self.active.value if self.active else None
        }

    def __repr__(self) -> str:
        return f"<Chat(id={self.id}, chat_ticket_id={self.chat_ticket_id})>"
