from datetime import date, datetime

from infra.configs.connection import DBConnectionHandler
from infra.entities.project import Project
from infra.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """
    Repositório para operações com Project.

    Herda de BaseRepository:
    - select_all(), select_by_id()
    - insert(), update()
    - soft_delete(), restore()
    - count(), exists()
    """

    def __init__(self):
        super().__init__(Project)

    # =========================================================================
    # MÉTODOS ESPECÍFICOS DE PROJECT
    # =========================================================================

    def create(self, project_name: str, project_directory: str, project_description: str,
               project_team_responsible_id: int, project_manager_id: int,
               project_tags, project_status, project_start_date: date,
               project_expected_end_date: date, project_planned_budget: float,
               project_public: bool = True) -> int:
        """
        Cria um novo projeto.

        Args:
            project_name: Nome do projeto (obrigatório, único)
            project_directory: Diretório do projeto (obrigatório, único)
            project_description: Descrição
            project_team_responsible_id: ID do time responsável
            project_manager_id: ID do gerente
            project_tags: Tags de classificação (enum ProjectTags)
            project_status: Status operacional (enum ProjectStatus)
            project_start_date: Data de início
            project_expected_end_date: Data prevista de término
            project_planned_budget: Orçamento planejado
            project_public: Se é público (default True)

        Returns:
            ID do projeto criado
        """
        project = Project(
            project_name=project_name,
            project_directory=project_directory,
            project_description=project_description,
            project_team_responsible_id=project_team_responsible_id,
            project_manager_id=project_manager_id,
            project_tags=project_tags,
            project_status=project_status,
            project_start_date=project_start_date,
            project_expected_end_date=project_expected_end_date,
            project_planned_budget=project_planned_budget
        )
        # Campo com init=False precisa ser setado após construção
        project.project_public = project_public
        return self.insert(project)

    def select_by_team(self, team_id: int) -> list[dict]:
        """Retorna projetos de um time específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Project.project_team_responsible_id == team_id
            ).all()
            return [item.to_dict() for item in data]

    def select_by_manager(self, manager_id: int) -> list[dict]:
        """Retorna projetos de um gerente específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Project.project_manager_id == manager_id
            ).all()
            return [item.to_dict() for item in data]

    def update_status(self, project_id: int, project_status, changed_by_id: int | None = None) -> bool:
        """Atualiza o status operacional do projeto."""
        return self.update(
            project_id,
            project_status=project_status,
            project_status_changed_by_id=changed_by_id,
            project_status_changed_at=datetime.now()
        )

    def approve(self, project_id: int, approved_budget: float) -> bool:
        """Marca projeto como aprovado."""
        return self.update(
            project_id,
            project_approved_at=date.today(),
            project_approved_budget=approved_budget
        )

    def complete(self, project_id: int, final_budget: float) -> bool:
        """Marca projeto como concluído."""
        return self.update(
            project_id,
            project_real_end_date=date.today(),
            project_final_budget=final_budget
        )
