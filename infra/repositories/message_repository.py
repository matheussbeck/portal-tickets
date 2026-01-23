from datetime import datetime

from infra.configs.connection import DBConnectionHandler
from infra.entities.message import Message
from infra.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """
    Repositório para operações com Message.

    Herda de BaseRepository:
    - select_all(), select_by_id()
    - insert(), update()
    - soft_delete(), restore()
    - count(), exists()
    """

    def __init__(self):
        super().__init__(Message)

    # =========================================================================
    # MÉTODOS ESPECÍFICOS DE MESSAGE
    # =========================================================================

    def create(self, message_chat_id: int, message_user_id: int, message_content: str,
               message_type: str = "text", message_is_internal: bool = False) -> int:
        """
        Cria uma nova mensagem.

        Args:
            message_chat_id: ID do chat
            message_user_id: ID do usuário que enviou
            message_content: Conteúdo da mensagem
            message_type: Tipo (text, file, system, status_change)
            message_is_internal: Se é mensagem interna (não visível para cliente)

        Returns:
            ID da mensagem criada
        """
        message = Message(
            message_chat_id=message_chat_id,
            message_user_id=message_user_id,
            message_content=message_content
        )
        # Campos com init=False precisam ser setados após criação
        message.message_type = message_type
        message.message_is_internal = message_is_internal
        return self.insert(message)

    def select_by_chat_id(self, chat_id: int) -> list[dict]:
        """Retorna mensagens de um chat específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Message.message_chat_id == chat_id
            ).order_by(Message.created_at).all()
            return [item.to_dict() for item in data]

    def select_by_user_id(self, user_id: int) -> list[dict]:
        """Retorna mensagens de um usuário específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Message.message_user_id == user_id
            ).all()
            return [item.to_dict() for item in data]

    def select_public_by_chat_id(self, chat_id: int) -> list[dict]:
        """Retorna apenas mensagens públicas de um chat."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Message.message_chat_id == chat_id,
                Message.message_is_internal == False
            ).order_by(Message.created_at).all()
            return [item.to_dict() for item in data]

    def update_content(self, message_id: int, message_content: str) -> bool:
        """Atualiza o conteúdo da mensagem."""
        return self.update(
            message_id,
            message_content=message_content,
            message_edited_at=datetime.now()
        )
