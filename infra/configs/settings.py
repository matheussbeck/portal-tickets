from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configurações da aplicação.

    Variáveis são carregadas de:
    1. Variáveis de ambiente do sistema (prioridade máxima)
    2. Arquivo .env no diretório raiz

    Prioridade: variável de ambiente do sistema > .env > valor default

    REGRA DE DESIGN:
    - Variáveis CRÍTICAS (banco, segurança): sem default → app crasha se faltar
    - Variáveis com valor sensato padrão: com default → funciona sem configurar
    """

    # Aplicação
    APP_NAME: str = Field(...,
                          description="Nome do App")
    DEBUG: bool = Field(...)

    # Banco de dados
    DATABASE_URL: str = Field(
        ...,description="URL de conexão com o banco"
    )

    # Segurança
    SECRET_KEY: str = Field(
        ..., min_length=32,description="Secret Key JWT"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(...)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(...)

    class Config:
        env_file = ".env" # Arquivo de onde lê as variáveis
        case_sensitive = True
        extra = "ignore" # Ignora variáveis extras no .env


@lru_cache  # Garante que Settings() é chamado só uma vez
def get_settings() -> Settings:
    return Settings()

# =========================================================================
# INSTÂNCIA GLOBAL - Importe assim:
# from infra.configs.settings import settings
# =========================================================================
settings = get_settings()