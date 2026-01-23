from datetime import datetime

from infra.configs.connection import DBConnectionHandler
from infra.entities.report import Report
from infra.repositories.base_repository import BaseRepository


class ReportRepository(BaseRepository[Report]):
    """
    Repositório para operações com Report.

    Herda de BaseRepository:
    - select_all(), select_by_id()
    - insert(), update()
    - soft_delete(), restore()
    - count(), exists()
    """

    def __init__(self):
        super().__init__(Report)

    # =========================================================================
    # MÉTODOS ESPECÍFICOS DE REPORT
    # =========================================================================

    def create(self, report_name: str, report_link: str, report_description: str,
               report_frequency, report_team_responsible_id: int, report_owner_id: int,
               report_status, report_tags, report_public: bool = True) -> int:
        """
        Cria um novo relatório.

        Args:
            report_name: Nome do relatório (obrigatório, único)
            report_link: Link do Power BI (obrigatório, único)
            report_description: Descrição
            report_frequency: Frequência de atualização (enum ReportFrequency)
            report_team_responsible_id: ID do time responsável
            report_owner_id: ID do dono
            report_status: Status operacional (enum ReportStatus)
            report_tags: Tags de classificação (enum ReportTags)
            report_public: Se é público (default True)

        Returns:
            ID do relatório criado
        """
        report = Report(
            report_name=report_name,
            report_link=report_link,
            report_description=report_description,
            report_frequency=report_frequency,
            report_team_responsible_id=report_team_responsible_id,
            report_owner_id=report_owner_id,
            report_status=report_status,
            report_tags=report_tags,
            report_public=report_public
        )
        return self.insert(report)

    def select_by_team(self, team_id: int) -> list[dict]:
        """Retorna relatórios de um time específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Report.report_team_responsible_id == team_id
            ).all()
            return [item.to_dict() for item in data]

    def select_by_owner(self, owner_id: int) -> list[dict]:
        """Retorna relatórios de um owner específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Report.report_owner_id == owner_id
            ).all()
            return [item.to_dict() for item in data]

    def update_status(self, report_id: int, report_status, changed_by_id: int | None = None) -> bool:
        """Atualiza o status operacional do relatório."""
        return self.update(
            report_id,
            report_status=report_status,
            report_status_changed_by_id=changed_by_id,
            report_status_changed_at=datetime.now()
        )
