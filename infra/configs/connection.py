"""
Gerenciador de conexão com o banco de dados.

Uso com Context Manager:
    with DBConnectionHandler() as db:
        db.session.query(User).all()
        # commit automático se não houver exceção
        # rollback automático se houver exceção
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from infra.configs.settings import settings


class DBConnectionHandler:
    """
    Context manager para conexões com o banco.

    Por que Context Manager?
    - Garante que conexão seja SEMPRE fechada
    - Commit/rollback automático baseado em exceções
    - Evita "connection leak" (conexões órfãs)
    """

    def __init__(self):
        self._engine = create_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,     # True = loga SQL (útil em dev)
            pool_pre_ping=True       # Verifica se conexão está viva
        )
        self._Session = sessionmaker(bind=self._engine)
        self.session: Session | None = None

    def __enter__(self) -> "DBConnectionHandler":
        """Abre sessão quando entra no 'with'."""
        self.session = self._Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Fecha sessão quando sai do 'with'.

        - Se houve exceção → rollback
        - Se não houve exceção → commit
        """
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def get_engine(self):
        """Retorna engine para criação de tabelas (usado pelo Alembic)."""
        return self._engine


def get_db():
    """
    Dependency injection para FastAPI.

    Uso:
        @app.get("/users")
        def list_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    handler = DBConnectionHandler()
    try:
        handler.session = handler._Session()
        yield handler.session
    finally:
        handler.session.close()
