from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TeamSchema(BaseModel):
    id: int
    team_name: str
    team_description: str
    team_area: str
    team_manager_id: int
    team_location: str
    team_cost_center: int
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int
    deleted_at: datetime
    deleted_by: int
    active: bool
    
    model_config = ConfigDict(from_attributes=True)