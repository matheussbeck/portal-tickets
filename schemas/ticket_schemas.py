from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TicketSchema(BaseModel):
    id: int
    ticket_title: str
    ticket_description: str
    ticket_class: str
    ticket_type: str
    ticket_priority: str
    ticket_impact:str 
    ticket_client_id: int
    ticket_form_id: int
    ticket_project_id: int
    ticket_report_id: int
    ticket_status: str
    ticket_status_changed_at: datetime
    ticket_status_changed_by_id: int
    ticket_deadline: datetime
    ticket_closed_at: datetime
    ticket_closed_by_id: int
    ticket_mail_sent_at: datetime
    ticket_estimated_hours: int
    ticket_actual_hours:int
    ticket_satisfaction_rating: int
    ticket_attachments: str
    ticket_resolution_notes: str
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int
    deleted_at: datetime
    deleted_by: int
    active: bool

    model_config = ConfigDict(from_attributes=True)