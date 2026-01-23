"""
Repositório base com operações CRUD e suporte a soft delete.

Todas as entidades herdam de Base que possui:
- active: Status (ATIVO/INATIVO) - usado para soft delete
- deleted_at: datetime - quando foi "deletado"
- deleted_by: int - quem "deletou"

Regra de Ouro:
- NUNCA execute DELETE real no banco
- Use soft_delete() que marca active=INATIVO
- Todas as queries filtram por active != INATIVO automaticamente
"""
from datetime import datetime
from typing import TypeVar, Generic, Type, List, Optional, Any

from sqlalchemy.orm import Session

from infra.configs.connection import DBConnectionHandler
from infra.configs.database import Base, Status

# Generic type para a entidade
T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Repositório base genérico com CRUD e soft delete.

    Uso:
        class UserRepository(BaseRepository[User]):
            def __init__(self):
                super().__init__(User)

            # Métodos específicos de User...
    """

    def __init__(self, model: Type[T]):
        self.model = model

    # =========================================================================
    # QUERIES BASE (com filtro de soft delete)
    # =========================================================================

    def _base_query(self, session: Session):
        """Query base que filtra registros soft-deleted."""
        return session.query(self.model).filter(self.model.active != Status.INATIVO)

    def _base_query_all(self, session: Session):
        """Query que inclui TODOS os registros (inclusive soft-deleted)."""
        return session.query(self.model)

    # =========================================================================
    # SELECT
    # =========================================================================

    def select_all(self, include_inactive: bool = False) -> List[dict]:
        """
        Retorna todos os registros ativos.

        Args:
            include_inactive: Se True, inclui registros soft-deleted
        """
        with DBConnectionHandler() as db:
            if include_inactive:
                data = self._base_query_all(db.session).all()
            else:
                data = self._base_query(db.session).all()
            return [item.to_dict() for item in data]

    def select_by_id(self, id: int, include_inactive: bool = False) -> Optional[dict]:
        """
        Retorna registro por ID.

        Args:
            id: ID do registro
            include_inactive: Se True, inclui registros soft-deleted
        """
        with DBConnectionHandler() as db:
            if include_inactive:
                query = self._base_query_all(db.session)
            else:
                query = self._base_query(db.session)
            data = query.filter(self.model.id == id).first()
            return data.to_dict() if data else None

    def exists(self, id: int) -> bool:
        """Verifica se registro existe (e está ativo)."""
        with DBConnectionHandler() as db:
            return self._base_query(db.session).filter(self.model.id == id).first() is not None

    def count(self, include_inactive: bool = False) -> int:
        """Conta registros."""
        with DBConnectionHandler() as db:
            if include_inactive:
                return self._base_query_all(db.session).count()
            return self._base_query(db.session).count()

    # =========================================================================
    # INSERT
    # =========================================================================

    def insert(self, entity: T) -> int:
        """
        Insere uma nova entidade.

        Args:
            entity: Instância da entidade a ser inserida

        Returns:
            ID do registro criado
        """
        with DBConnectionHandler() as db:
            db.session.add(entity)
            db.session.flush()
            db.session.refresh(entity)
            return entity.id

    # =========================================================================
    # UPDATE
    # =========================================================================

    def update(self, id: int, updated_by: Optional[int] = None, **kwargs) -> bool:
        """
        Atualiza campos específicos de um registro.

        Args:
            id: ID do registro
            updated_by: ID do usuário que está atualizando
            **kwargs: Campos a serem atualizados

        Returns:
            True se atualizou, False se não encontrou
        """
        with DBConnectionHandler() as db:
            query = self._base_query(db.session).filter(self.model.id == id)
            if query.first() is None:
                return False

            if updated_by:
                kwargs['updated_by'] = updated_by

            query.update(kwargs)
            return True

    # =========================================================================
    # SOFT DELETE
    # =========================================================================

    def soft_delete(self, id: int, deleted_by: Optional[int] = None) -> bool:
        """
        Marca registro como inativo (soft delete).

        Args:
            id: ID do registro
            deleted_by: ID do usuário que está deletando

        Returns:
            True se deletou, False se não encontrou
        """
        with DBConnectionHandler() as db:
            query = self._base_query(db.session).filter(self.model.id == id)
            if query.first() is None:
                return False

            query.update({
                self.model.active: Status.INATIVO,
                self.model.deleted_at: datetime.now(),
                self.model.deleted_by: deleted_by
            })
            return True

    def restore(self, id: int) -> bool:
        """
        Restaura registro soft-deleted.

        Args:
            id: ID do registro

        Returns:
            True se restaurou, False se não encontrou
        """
        with DBConnectionHandler() as db:
            query = self._base_query_all(db.session).filter(
                self.model.id == id,
                self.model.active == Status.INATIVO
            )
            if query.first() is None:
                return False

            query.update({
                self.model.active: Status.ATIVO,
                self.model.deleted_at: None,
                self.model.deleted_by: None
            })
            return True

    # =========================================================================
    # HARD DELETE (usar com cautela!)
    # =========================================================================

    def hard_delete(self, id: int) -> bool:
        """
        Remove registro PERMANENTEMENTE do banco.

        ATENÇÃO: Use apenas em casos excepcionais!
        Prefira sempre soft_delete().

        Args:
            id: ID do registro

        Returns:
            True se deletou, False se não encontrou
        """
        with DBConnectionHandler() as db:
            query = db.session.query(self.model).filter(self.model.id == id)
            if query.first() is None:
                return False
            query.delete()
            return True

    # =========================================================================
    # MÉTODOS DE RELACIONAMENTO (para subclasses)
    # =========================================================================

    def get_entity_by_id(self, id: int, include_inactive: bool = False) -> Optional[T]:
        """
        Retorna a entidade ORM (não dict) para manipulação de relacionamentos.

        Args:
            id: ID do registro
            include_inactive: Se True, inclui registros soft-deleted

        Returns:
            Entidade ORM ou None
        """
        with DBConnectionHandler() as db:
            if include_inactive:
                query = self._base_query_all(db.session)
            else:
                query = self._base_query(db.session)
            return query.filter(self.model.id == id).first()
