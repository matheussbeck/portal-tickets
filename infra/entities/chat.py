from sqlalchemy import ForeignKey, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.configs.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infra.entities.ticket import Ticket
    from infra.entities.message import Message


class Chat(Base):
    """
    Container de mensagens para um ticket.

    Cada ticket tem exatamente um chat associado (1-1).
    O chat agrupa todas as mensagens trocadas sobre o ticket.

    Relacionamentos:
        N-1 (Chat pertence a):
            - ticket: Ticket ao qual o chat está vinculado

        1-N (Chat possui muitos):
            - messages: Mensagens do chat

    Índices:
        - ix_chats_ticket: Índice único pelo ticket_id

    Exemplo de Instanciação (Template Construtor):
        ```python
        # Campos OBRIGATÓRIOS no construtor:
        chat = Chat(
            chat_ticket_id=1  # FK para Ticket (unique)
        )

        # Campos OPCIONAIS (têm init=False):
        # - chat_title: Título opcional do chat
        ```
    """
    __tablename__ = "chats"

    # O índice único já está no campo (unique=True)
    __table_args__ = (
        Index('ix_chats_ticket', 'chat_ticket_id', unique=True),
    )

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    chat_ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
        doc="FK para Ticket (unique - relação 1-1)"
    )

    # =========================================================================
    # EXTRAS
    # =========================================================================
    chat_title: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="Título opcional do chat (geralmente igual ao título do ticket)"
    )

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
