from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ReportSchema(BaseModel):
    id: int
    report_name: str
    report_link: str
    report_description: str
    report_frequency: str
    report_tags: str
    report_team_responsible_id: int
    report_owner_id: int
    report_status: str
    report_status_changed_at: datetime 
    report_status_changed_by_id: int
    report_data_last_update: datetime
    report_pbix_last_update: datetime
    report_public: bool
    report_dataset_source: str
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int
    deleted_at: datetime
    deleted_by:int 
    active: bool
    
    model_config = ConfigDict(from_attributes=True)