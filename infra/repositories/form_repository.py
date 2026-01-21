from infra.configs.connection import DBConnectionHandler
from infra.entities.form import Form


class FormRepository:
    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Form).all()
            return [item.to_dict() for item in data]

    def select_by_id(self, form_id: int):
        with DBConnectionHandler() as db:
            data = db.session.query(Form).filter(Form.id == form_id).first()
            return data.to_dict() if data else None

    def insert(self, form_name: str, form_ticket_class, form_type, form_fields: str):
        """
        Obrigatórios: form_name, form_ticket_class, form_type, form_fields
        """
        with DBConnectionHandler() as db:
            data = Form(
                form_name=form_name,
                form_ticket_class=form_ticket_class,
                form_type=form_type,
                form_fields=form_fields
            )
            db.session.add(data)
            db.session.flush()
            db.session.refresh(data)
            return data.id

    def delete(self, form_id: int):
        with DBConnectionHandler() as db:
            db.session.query(Form).filter(Form.id == form_id).delete()

    def update(self, form_id: int, **kwargs):
        """Atualiza campos específicos do formulário"""
        with DBConnectionHandler() as db:
            db.session.query(Form).filter(Form.id == form_id).update(kwargs)

    def update_fields(self, form_id: int, form_fields: str):
        with DBConnectionHandler() as db:
            db.session.query(Form).filter(Form.id == form_id).update({
                Form.form_fields: form_fields
            })
