from infra.configs.connection import DBConnectionHandler
from infra.entities.message import Message


class MessageRepository:
    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Message).all()
            return [item.to_dict() for item in data]

    def select_by_id(self, message_id: int):
        with DBConnectionHandler() as db:
            data = db.session.query(Message).filter(Message.id == message_id).first()
            return data.to_dict() if data else None

    def select_by_chat_id(self, chat_id: int):
        with DBConnectionHandler() as db:
            data = db.session.query(Message).filter(Message.message_chat_id == chat_id).all()
            return [item.to_dict() for item in data]

    def insert(self, message_chat_id: int, message_user_id: int, message_content: str,
               message_type: str = "text", message_is_internal: bool = False):
        """
        Obrigatórios: message_chat_id, message_user_id, message_content
        """
        with DBConnectionHandler() as db:
            data = Message(
                message_chat_id=message_chat_id,
                message_user_id=message_user_id,
                message_content=message_content,
                message_type=message_type,
                message_is_internal=message_is_internal
            )
            db.session.add(data)
            db.session.flush()
            db.session.refresh(data)
            return data.id

    def delete(self, message_id: int):
        with DBConnectionHandler() as db:
            db.session.query(Message).filter(Message.id == message_id).delete()

    def update(self, message_id: int, **kwargs):
        """Atualiza campos específicos da mensagem"""
        with DBConnectionHandler() as db:
            db.session.query(Message).filter(Message.id == message_id).update(kwargs)

    def update_content(self, message_id: int, message_content: str):
        from datetime import datetime
        with DBConnectionHandler() as db:
            db.session.query(Message).filter(Message.id == message_id).update({
                Message.message_content: message_content,
                Message.message_edited_at: datetime.now()
            })
