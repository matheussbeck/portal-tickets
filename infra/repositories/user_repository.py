from infra.configs.connection import DBConnectionHandler
from infra.entities.user import User


class UserRepository:
    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(User).all()
            return [item.to_dict() for item in data]

    def select_by_id(self, user_id: int):
        with DBConnectionHandler() as db:
            data = db.session.query(User).filter(User.id == user_id).first()
            return data.to_dict() if data else None

    def select_by_email(self, user_email: str):
        with DBConnectionHandler() as db:
            data = db.session.query(User).filter(User.user_email == user_email).first()
            return data.to_dict() if data else None

    def insert(self, user_corporative_id: int, user_full_name: str, user_email: str,
               user_password: str, user_team_id: int, user_role, user_tipo):
        """
        Obrigatórios: user_corporative_id, user_full_name, user_email, user_password, user_team_id, user_role, user_tipo
        """
        with DBConnectionHandler() as db:
            data = User(
                user_corporative_id=user_corporative_id,
                user_full_name=user_full_name,
                user_email=user_email,
                user_password=user_password,
                user_team_id=user_team_id,
                user_role=user_role,
                user_tipo=user_tipo
            )
            db.session.add(data)
            db.session.flush()
            db.session.refresh(data)
            return data.id

    def delete(self, user_id: int):
        with DBConnectionHandler() as db:
            db.session.query(User).filter(User.id == user_id).delete()

    def update(self, user_id: int, **kwargs):
        """Atualiza campos específicos do usuário"""
        with DBConnectionHandler() as db:
            db.session.query(User).filter(User.id == user_id).update(kwargs)

    def update_password(self, user_id: int, user_password: str):
        with DBConnectionHandler() as db:
            db.session.query(User).filter(User.id == user_id).update({
                User.user_password: user_password
            })
