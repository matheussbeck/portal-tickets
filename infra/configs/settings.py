from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configurações da aplicação.

    Variáveis são carregadas de:
    1. Variáveis de ambiente do sistema
    2. Arquivo .env no diretório raiz

    Prioridade: variável de ambiente > .env > valor default
    """

    # Aplicação
    APP_NAME: str = "Portal de Chamados"
    DEBUG: bool = False  # "true"/"false" convertido automaticamente

    # Banco de dados
    DATABASE_URL: str = "sqlite:///./app.db"

    # Segurança
    SECRET_KEY: str = "sua-chave-secreta-aqui"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # "30" convertido para int

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """Retorna settings cacheado."""
    return Settings()


# Instância global
settings = get_settings()