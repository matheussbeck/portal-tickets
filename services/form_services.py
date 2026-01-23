from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FormSchema(BaseModel):

    id: int
    form_name: str
    form_description: str
    form_ticket_class: str
    form_type: str
    form_fields: str
    form_is_default: str
    form_version: str
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int
    deleted_at: datetime
    deleted_by: int
    active: bool
    
    model_config = ConfigDict(from_attributes=True)