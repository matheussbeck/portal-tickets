from infra.configs.connection import DBConnectionHandler
from infra.entities.ticket import Ticket


class TicketRepository:
    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Ticket).all()
            return [item.to_dict() for item in data]

    def select_by_id(self, ticket_id: int):
        with DBConnectionHandler() as db:
            data = db.session.query(Ticket).filter(Ticket.id == ticket_id).first()
            return data.to_dict() if data else None

    def insert(self, ticket_title: str, ticket_class, ticket_type,
               ticket_client_id: int, ticket_description: str,
               ticket_form_id: int, ticket_status):
        """
        Obrigatórios: ticket_title, ticket_class, ticket_type, ticket_client_id,
                      ticket_description, ticket_form_id, ticket_status
        """
        with DBConnectionHandler() as db:
            data = Ticket(
                ticket_title=ticket_title,
                ticket_class=ticket_class,
                ticket_type=ticket_type,
                ticket_client_id=ticket_client_id,
                ticket_description=ticket_description,
                ticket_form_id=ticket_form_id,
                ticket_status=ticket_status
            )
            db.session.add(data)
            db.session.flush()
            db.session.refresh(data)
            return data.id

    def delete(self, ticket_id: int):
        with DBConnectionHandler() as db:
            db.session.query(Ticket).filter(Ticket.id == ticket_id).delete()

    def update(self, ticket_id: int, **kwargs):
        """Atualiza campos específicos do ticket"""
        with DBConnectionHandler() as db:
            db.session.query(Ticket).filter(Ticket.id == ticket_id).update(kwargs)

    def update_status(self, ticket_id: int, ticket_status, changed_by_id: int | None = None):
        from datetime import datetime
        with DBConnectionHandler() as db:
            db.session.query(Ticket).filter(Ticket.id == ticket_id).update({
                Ticket.ticket_status: ticket_status,
                Ticket.ticket_status_changed_by_id: changed_by_id,
                Ticket.ticket_status_changed_at: datetime.now()
            })

    def close(self, ticket_id: int, closed_by_id: int, resolution_notes: str | None = None):
        """Fecha um ticket"""
        from datetime import datetime
        with DBConnectionHandler() as db:
            db.session.query(Ticket).filter(Ticket.id == ticket_id).update({
                Ticket.ticket_closed_by_id: closed_by_id,
                Ticket.ticket_closed_at: datetime.now(),
                Ticket.ticket_resolution_notes: resolution_notes
            })

    def assign_to_project(self, ticket_id: int, project_id: int):
        """Associa ticket a um projeto"""
        with DBConnectionHandler() as db:
            db.session.query(Ticket).filter(Ticket.id == ticket_id).update({
                Ticket.ticket_project_id: project_id
            })

    def assign_to_report(self, ticket_id: int, report_id: int):
        """Associa ticket a um relatório"""
        with DBConnectionHandler() as db:
            db.session.query(Ticket).filter(Ticket.id == ticket_id).update({
                Ticket.ticket_report_id: report_id
            })
