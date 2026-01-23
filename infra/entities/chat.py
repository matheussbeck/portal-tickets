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
        ForeignKey("tickets.id", ondelete="RESTRICT"),
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

    def __repr__(self) -> str:
        return f"<Chat(id={self.id}, chat_ticket_id={self.chat_ticket_id})>"
