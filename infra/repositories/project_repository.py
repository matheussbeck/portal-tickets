from infra.configs.connection import DBConnectionHandler
from infra.entities.project import Project
from datetime import date


class ProjectRepository:
    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Project).all()
            return [item.to_dict() for item in data]

    def select_by_id(self, project_id: int):
        with DBConnectionHandler() as db:
            data = db.session.query(Project).filter(Project.id == project_id).first()
            return data.to_dict() if data else None

    def insert(self, project_name: str, project_directory: str, project_description: str,
               project_team_responsible_id: int, project_manager_id: int,
               project_tags, project_status, project_start_date: date,
               project_expected_end_date: date, project_planned_budget: float,
               project_public: bool = True):
        """
        Obrigatórios: project_name, project_directory, project_description,
                      project_team_responsible_id, project_manager_id, project_tags,
                      project_status, project_start_date, project_expected_end_date,
                      project_planned_budget
        """
        with DBConnectionHandler() as db:
            data = Project(
                project_name=project_name,
                project_directory=project_directory,
                project_description=project_description,
                project_team_responsible_id=project_team_responsible_id,
                project_manager_id=project_manager_id,
                project_tags=project_tags,
                project_status=project_status,
                project_start_date=project_start_date,
                project_expected_end_date=project_expected_end_date,
                project_planned_budget=project_planned_budget,
                project_public=project_public
            )
            db.session.add(data)
            db.session.flush()
            db.session.refresh(data)
            return data.id

    def delete(self, project_id: int):
        with DBConnectionHandler() as db:
            db.session.query(Project).filter(Project.id == project_id).delete()

    def update(self, project_id: int, **kwargs):
        """Atualiza campos específicos do projeto"""
        with DBConnectionHandler() as db:
            db.session.query(Project).filter(Project.id == project_id).update(kwargs)

    def update_status(self, project_id: int, project_status, changed_by_id: int | None = None):
        from datetime import datetime
        with DBConnectionHandler() as db:
            db.session.query(Project).filter(Project.id == project_id).update({
                Project.project_status: project_status,
                Project.project_status_changed_by_id: changed_by_id,
                Project.project_status_changed_at: datetime.now()
            })

    def approve(self, project_id: int, approved_budget: float):
        """Marca projeto como aprovado"""
        with DBConnectionHandler() as db:
            db.session.query(Project).filter(Project.id == project_id).update({
                Project.project_approved_at: date.today(),
                Project.project_approved_budget: approved_budget
            })

    def complete(self, project_id: int, final_budget: float):
        """Marca projeto como concluído"""
        with DBConnectionHandler() as db:
            db.session.query(Project).filter(Project.id == project_id).update({
                Project.project_real_end_date: date.today(),
                Project.project_final_budget: final_budget
            })
