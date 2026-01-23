from infra.configs.connection import DBConnectionHandler
from infra.entities.team import Team
from infra.repositories.base_repository import BaseRepository


class TeamRepository(BaseRepository[Team]):
    """
    Repositório para operações com Team.

    Herda de BaseRepository:
    - select_all(), select_by_id()
    - insert(), update()
    - soft_delete(), restore()
    - count(), exists()
    """

    def __init__(self):
        super().__init__(Team)

    # =========================================================================
    # MÉTODOS ESPECÍFICOS DE TEAM
    # =========================================================================

    def create(self, team_name: str, team_area) -> int:
        """
        Cria um novo time.

        Args:
            team_name: Nome do time (obrigatório, único)
            team_area: Área do time (enum Area)

        Returns:
            ID do time criado
        """
        team = Team(
            team_name=team_name,
            team_area=team_area
        )
        return self.insert(team)

    def set_manager(self, team_id: int, manager_id: int | None) -> bool:
        """
        Define o gerente do time.

        Args:
            team_id: ID do time
            manager_id: ID do usuário gerente (ou None para remover)

        Returns:
            True se atualizou, False se não encontrou
        """
        return self.update(team_id, team_manager_id=manager_id)

    def select_by_area(self, area) -> list[dict]:
        """Retorna times de uma área específica."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(Team.team_area == area).all()
            return [item.to_dict() for item in data]

    def select_by_name(self, team_name: str) -> dict | None:
        """Busca time pelo nome."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(Team.team_name == team_name).first()
            return data.to_dict() if data else None
