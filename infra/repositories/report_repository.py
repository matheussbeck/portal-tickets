from infra.configs.connection import DBConnectionHandler
from infra.entities.report import Report


class ReportRepository:
    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Report).all()
            return [item.to_dict() for item in data]

    def select_by_id(self, report_id: int):
        with DBConnectionHandler() as db:
            data = db.session.query(Report).filter(Report.id == report_id).first()
            return data.to_dict() if data else None

    def insert(self, report_name: str, report_link: str, report_description: str,
               report_frequency, report_team_responsible_id: int, report_owner_id: int,
               report_status, report_tags, report_public: bool = True):
        """
        Obrigatórios: report_name, report_link, report_description, report_frequency,
                      report_team_responsible_id, report_owner_id, report_status, report_tags
        """
        with DBConnectionHandler() as db:
            data = Report(
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
            db.session.add(data)
            db.session.flush()
            db.session.refresh(data)
            return data.id

    def delete(self, report_id: int):
        with DBConnectionHandler() as db:
            db.session.query(Report).filter(Report.id == report_id).delete()

    def update(self, report_id: int, **kwargs):
        """Atualiza campos específicos do relatório"""
        with DBConnectionHandler() as db:
            db.session.query(Report).filter(Report.id == report_id).update(kwargs)

    def update_status(self, report_id: int, report_status, changed_by_id: int | None = None):
        from datetime import datetime
        with DBConnectionHandler() as db:
            db.session.query(Report).filter(Report.id == report_id).update({
                Report.report_status: report_status,
                Report.report_status_changed_by_id: changed_by_id,
                Report.report_status_changed_at: datetime.now()
            })
