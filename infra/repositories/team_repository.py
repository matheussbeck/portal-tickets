from sqlalchemy import inspect
from infra.configs.connection import DBConnectionHandler
from infra.entities.team import Team


class TeamRepository:
    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Team).all()
            return [item.to_dict() for item in data]

    def select_by_id(self, team_id: int):
        with DBConnectionHandler() as db:
            data = db.session.query(Team).filter(Team.id == team_id).first()
            return data.to_dict() if data else None

    def insert(self, team_name: str, team_area):
        """
        Obrigatórios: team_name, team_area
        """
        with DBConnectionHandler() as db:
            data = Team(
                team_name=team_name,
                team_area=team_area
            )
            db.session.add(data)
            db.session.flush()
            db.session.refresh(data)
            return inspect(data).identity[0]

    def delete(self, team_id: int):
        with DBConnectionHandler() as db:
            db.session.query(Team).filter(Team.id == team_id).delete()

    def update(self, team_id: int, **kwargs):
        """Atualiza campos específicos do time"""
        with DBConnectionHandler() as db:
            db.session.query(Team).filter(Team.id == team_id).update(kwargs)

    def set_manager(self, team_id: int, manager_id: int | None):
        """Define o gerente do time"""
        with DBConnectionHandler() as db:
            db.session.query(Team).filter(Team.id == team_id).update({
                Team.team_manager_id: manager_id
            })
