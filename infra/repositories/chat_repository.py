from infra.configs.connection import DBConnectionHandler
from infra.entities.chat import Chat
from infra.repositories.base_repository import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    """
    Repositório para operações com Chat.

    Herda de BaseRepository:
    - select_all(), select_by_id()
    - insert(), update()
    - soft_delete(), restore()
    - count(), exists()
    """

    def __init__(self):
        super().__init__(Chat)

    # =========================================================================
    # MÉTODOS ESPECÍFICOS DE CHAT
    # =========================================================================

    def create(self, chat_ticket_id: int) -> int:
        """
        Cria um novo chat para um ticket.

        Args:
            chat_ticket_id: ID do ticket (obrigatório, único)

        Returns:
            ID do chat criado
        """
        chat = Chat(chat_ticket_id=chat_ticket_id)
        return self.insert(chat)

    def select_by_ticket_id(self, ticket_id: int) -> dict | None:
        """Busca chat pelo ID do ticket."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Chat.chat_ticket_id == ticket_id
            ).first()
            return data.to_dict() if data else None

    def update_title(self, chat_id: int, chat_title: str) -> bool:
        """Atualiza o título do chat."""
        return self.update(chat_id, chat_title=chat_title)
