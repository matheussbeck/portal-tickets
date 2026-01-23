from datetime import datetime

from infra.configs.connection import DBConnectionHandler
from infra.entities.ticket import Ticket
from infra.repositories.base_repository import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    """
    Repositório para operações com Ticket.

    Herda de BaseRepository:
    - select_all(), select_by_id()
    - insert(), update()
    - soft_delete(), restore()
    - count(), exists()
    """

    def __init__(self):
        super().__init__(Ticket)

    # =========================================================================
    # MÉTODOS ESPECÍFICOS DE TICKET
    # =========================================================================

    def create(self, ticket_title: str, ticket_class, ticket_type,
               ticket_client_id: int, ticket_description: str,
               ticket_form_id: int, ticket_status) -> int:
        """
        Cria um novo ticket.

        Args:
            ticket_title: Título do ticket
            ticket_class: Classe (PROJETO ou RELATORIO)
            ticket_type: Tipo (enum TicketTipo)
            ticket_client_id: ID do cliente que abriu
            ticket_description: Descrição do problema
            ticket_form_id: ID do formulário usado
            ticket_status: Status inicial (enum TicketStatus)

        Returns:
            ID do ticket criado
        """
        ticket = Ticket(
            ticket_title=ticket_title,
            ticket_class=ticket_class,
            ticket_type=ticket_type,
            ticket_client_id=ticket_client_id,
            ticket_description=ticket_description,
            ticket_form_id=ticket_form_id,
            ticket_status=ticket_status
        )
        return self.insert(ticket)

    def select_by_client(self, client_id: int) -> list[dict]:
        """Retorna tickets de um cliente específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Ticket.ticket_client_id == client_id
            ).all()
            return [item.to_dict() for item in data]

    def select_by_project(self, project_id: int) -> list[dict]:
        """Retorna tickets de um projeto específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Ticket.ticket_project_id == project_id
            ).all()
            return [item.to_dict() for item in data]

    def select_by_report(self, report_id: int) -> list[dict]:
        """Retorna tickets de um relatório específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Ticket.ticket_report_id == report_id
            ).all()
            return [item.to_dict() for item in data]

    def update_status(self, ticket_id: int, ticket_status, changed_by_id: int | None = None) -> bool:
        """Atualiza o status operacional do ticket."""
        return self.update(
            ticket_id,
            ticket_status=ticket_status,
            ticket_status_changed_by_id=changed_by_id,
            ticket_status_changed_at=datetime.now()
        )

    def close(self, ticket_id: int, closed_by_id: int, resolution_notes: str | None = None) -> bool:
        """Fecha um ticket."""
        return self.update(
            ticket_id,
            ticket_closed_by_id=closed_by_id,
            ticket_closed_at=datetime.now(),
            ticket_resolution_notes=resolution_notes
        )

    def assign_to_project(self, ticket_id: int, project_id: int) -> bool:
        """Associa ticket a um projeto."""
        return self.update(ticket_id, ticket_project_id=project_id)

    def assign_to_report(self, ticket_id: int, report_id: int) -> bool:
        """Associa ticket a um relatório."""
        return self.update(ticket_id, ticket_report_id=report_id)
