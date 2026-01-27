from sqlalchemy import ForeignKey, Integer, String, Boolean, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from infra.configs.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infra.entities.chat import Chat
    from infra.entities.user import User


class Message(Base):
    """
    Mensagem dentro de um chat de ticket.

    Representa uma comunicação entre usuários sobre um ticket.
    Pode ser texto, arquivo ou mensagem de sistema.

    Relacionamentos:
        N-1 (Message pertence a):
            - chat: Chat container da mensagem
            - user: Usuário que enviou a mensagem

    Índices:
        - ix_messages_chat: Mensagens de um chat (ordenadas por created_at)
        - ix_messages_user: Mensagens de um usuário

    Exemplo de Instanciação (Template Construtor):
        ```python
        # Campos OBRIGATÓRIOS no construtor:
        message = Message(
            message_chat_id=1,           # FK para Chat
            message_user_id=1,           # FK para User
            message_content="Olá..."     # Texto da mensagem
        )

        # Campos OPCIONAIS (têm init=False):
        # - message_type: 'text' por padrão ('file', 'system', 'status_change')
        # - message_attachments: JSON array de anexos
        # - message_is_internal: False por padrão (visível para cliente)
        # - message_edited_at: Se mensagem foi editada
        ```
    """
    __tablename__ = "messages"

    # Índices compostos para queries frequentes
    __table_args__ = (
        Index('ix_messages_chat', 'message_chat_id'),
        Index('ix_messages_user', 'message_user_id'),
    )

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    message_chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="RESTRICT"),
        nullable=False,
        doc="FK para Chat container da mensagem"
    )
    message_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        doc="FK para User que enviou a mensagem"
    )

    # =========================================================================
    # CONTEÚDO
    # =========================================================================
    message_content: Mapped[str] = mapped_column(
        String, nullable=False,
        doc="Conteúdo da mensagem (texto ou descrição do arquivo)"
    )
    message_type: Mapped[str] = mapped_column(
        String, default="text",
        init=False,
        doc="Tipo: 'text', 'file', 'system', 'status_change'"
    )
    message_attachments: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        init=False,
        doc="JSON array com URLs/paths dos arquivos anexados"
    )

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    message_is_internal: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        init=False,
        doc="Se True, mensagem interna (não visível para solicitante)"
    )

    # =========================================================================
    # DATAS
    # =========================================================================
    message_edited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
        doc="Data/hora da última edição (None se nunca editada)"
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
        foreign_keys=[message_user_id],
        back_populates="messages_sent",
        lazy="raise",
        init=False
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, message_chat_id={self.message_chat_id}, message_user_id={self.message_user_id})>"
