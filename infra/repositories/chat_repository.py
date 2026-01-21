from infra.configs.connection import DBConnectionHandler
from infra.entities.chat import Chat


class ChatRepository:
    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Chat).all()
            return [item.to_dict() for item in data]

    def select_by_id(self, chat_id: int):
        with DBConnectionHandler() as db:
            data = db.session.query(Chat).filter(Chat.id == chat_id).first()
            return data.to_dict() if data else None

    def select_by_ticket_id(self, ticket_id: int):
        with DBConnectionHandler() as db:
            data = db.session.query(Chat).filter(Chat.chat_ticket_id == ticket_id).first()
            return data.to_dict() if data else None

    def insert(self, chat_ticket_id: int):
        """
        Obrigatórios: chat_ticket_id
        """
        with DBConnectionHandler() as db:
            data = Chat(
                chat_ticket_id=chat_ticket_id
            )
            db.session.add(data)
            db.session.flush()
            db.session.refresh(data)
            return data.id

    def delete(self, chat_id: int):
        with DBConnectionHandler() as db:
            db.session.query(Chat).filter(Chat.id == chat_id).delete()

    def update_title(self, chat_id: int, chat_title: str):
        with DBConnectionHandler() as db:
            db.session.query(Chat).filter(Chat.id == chat_id).update({
                Chat.chat_title: chat_title
            })
