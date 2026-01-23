from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ChatSchema(BaseModel):

    id: int
    chat_ticket_id: int
    chat_title: str
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int
    deleted_at: datetime
    deleted_by: int
    active: bool
    
    model_config = ConfigDict(from_attributes=True)