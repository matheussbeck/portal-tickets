from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserSchema(BaseModel):
    id: int
    user_corporative_id: int
    user_full_name: str
    user_email: str
    user_photo: str
    user_team_id: int
    user_role: str
    user_tipo: str
    user_notification_preferences: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str
    deleted_at: datetime
    deleted_by: str
    active: bool
        
    model_config = ConfigDict(from_attributes=True)

# ═══ 1. UserList - Para listagens ═══
class UserList(BaseModel):
    """Mínimo para listar usuários"""
    id: int
    user_full_name: str
    user_email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ═══ 2. UserDetail - Para detalhes ═══
class UserDetail(BaseModel):
    """Mais campos, sem relacionamentos pesados"""
    id: int
    user_full_name: str
    user_email: str
    user_photo: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


# ═══ 3. UserWithTeam - Com relacionamento ═══
class TeamSimple(BaseModel):
    """Team simplificado (evita recursão)"""
    id: int
    team_name: str

    model_config = ConfigDict(from_attributes=True)


class UserWithTeam(BaseModel):
    """User com team incluído"""
    id: int
    user_full_name: str
    user_email: str
    is_active: bool
    team: TeamSimple  # Relationship incluído

    model_config = ConfigDict(from_attributes=True)


# ═══ 4. UserCreate - Para criação ═══
class UserCreate(BaseModel):
    """Dados necessários para criar user"""
    user_full_name: str
    user_email: str
    user_password: str
    user_team_id: int
    # Não inclui id, created_at (gerados automaticamente)


# ═══ 5. UserUpdate - Para atualização ═══
class UserUpdate(BaseModel):
    """Campos que podem ser atualizados (todos opcionais)"""
    user_full_name: str | None = None
    user_email: str | None = None
    user_photo: str | None = None
    is_active: bool | None = None

