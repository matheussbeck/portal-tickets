from infra.configs.connection import DBConnectionHandler
from infra.entities.user import User
from infra.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repositório para operações com User.

    Herda de BaseRepository:
    - select_all(), select_by_id()
    - insert(), update()
    - soft_delete(), restore()
    - count(), exists()
    """

    def __init__(self):
        super().__init__(User)

    # =========================================================================
    # MÉTODOS ESPECÍFICOS DE USER
    # =========================================================================

    def create(self, user_corporative_id: int, user_full_name: str, user_email: str,
               user_password: str, user_team_id: int, user_role, user_tipo) -> int:
        """
        Cria um novo usuário.

        Args:
            user_corporative_id: ID corporativo (obrigatório, único)
            user_full_name: Nome completo
            user_email: Email (obrigatório, único)
            user_password: Senha
            user_team_id: ID do time
            user_role: Role do usuário (enum UserRoles)
            user_tipo: Tipo do usuário (enum UserTipo)

        Returns:
            ID do usuário criado
        """
        user = User(
            user_corporative_id=user_corporative_id,
            user_full_name=user_full_name,
            user_email=user_email,
            user_password=user_password,
            user_team_id=user_team_id,
            user_role=user_role,
            user_tipo=user_tipo
        )
        return self.insert(user)

    def select_by_email(self, user_email: str) -> dict | None:
        """Busca usuário pelo email."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(User.user_email == user_email).first()
            return data.to_dict() if data else None

    def select_by_corporative_id(self, corporative_id: int) -> dict | None:
        """Busca usuário pelo ID corporativo."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(User.user_corporative_id == corporative_id).first()
            return data.to_dict() if data else None

    def select_by_team(self, team_id: int) -> list[dict]:
        """Retorna usuários de um time específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(User.user_team_id == team_id).all()
            return [item.to_dict() for item in data]

    def update_password(self, user_id: int, user_password: str) -> bool:
        """Atualiza a senha do usuário."""
        return self.update(user_id, user_password=user_password)

    def update_status(self, user_id: int, user_status) -> bool:
        """Atualiza o status operacional do usuário."""
        return self.update(user_id, user_status=user_status)
