from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MessageSchema(BaseModel):

    id: int
    message_chat_id: int
    message_user_id: int
    message_content: str
    message_type: str
    message_attachments: str
    message_is_internal: bool
    message_edited_at: datetime
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int
    deleted_at: datetime
    deleted_by: int
    active: bool
    
    model_config = ConfigDict(from_attributes=True)