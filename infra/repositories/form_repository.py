from infra.configs.connection import DBConnectionHandler
from infra.entities.form import Form
from infra.repositories.base_repository import BaseRepository


class FormRepository(BaseRepository[Form]):
    """
    Repositório para operações com Form.

    Herda de BaseRepository:
    - select_all(), select_by_id()
    - insert(), update()
    - soft_delete(), restore()
    - count(), exists()
    """

    def __init__(self):
        super().__init__(Form)

    # =========================================================================
    # MÉTODOS ESPECÍFICOS DE FORM
    # =========================================================================

    def create(self, form_name: str, form_ticket_class, form_type, form_fields: str) -> int:
        """
        Cria um novo formulário.

        Args:
            form_name: Nome do formulário
            form_ticket_class: Classe de ticket (PROJETO ou RELATORIO)
            form_type: Tipo de ticket (enum FormTipo)
            form_fields: JSON com definição dos campos

        Returns:
            ID do formulário criado
        """
        form = Form(
            form_name=form_name,
            form_ticket_class=form_ticket_class,
            form_type=form_type,
            form_fields=form_fields
        )
        return self.insert(form)

    def select_by_class(self, form_ticket_class) -> list[dict]:
        """Retorna formulários de uma classe específica."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Form.form_ticket_class == form_ticket_class
            ).all()
            return [item.to_dict() for item in data]

    def select_by_type(self, form_type) -> list[dict]:
        """Retorna formulários de um tipo específico."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Form.form_type == form_type
            ).all()
            return [item.to_dict() for item in data]

    def select_default(self, form_ticket_class, form_type) -> dict | None:
        """Retorna o formulário padrão para uma classe/tipo."""
        with DBConnectionHandler() as db:
            data = self._base_query(db.session).filter(
                Form.form_ticket_class == form_ticket_class,
                Form.form_type == form_type,
                Form.form_is_default == True
            ).first()
            return data.to_dict() if data else None

    def update_fields(self, form_id: int, form_fields: str) -> bool:
        """Atualiza os campos do formulário."""
        return self.update(form_id, form_fields=form_fields)

    def set_as_default(self, form_id: int) -> bool:
        """Marca um formulário como padrão."""
        return self.update(form_id, form_is_default=True)
