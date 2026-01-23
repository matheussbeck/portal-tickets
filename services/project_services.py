from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ProjectSchema(BaseModel):

    id: int
    project_name: str
    project_directory: str
    project_description: str
    project_category: str
    project_methodology: str
    project_tags: str 
    project_priority: str
    project_risk_level: str
    project_team_responsible_id: int
    project_manager_id: int
    project_status: str
    project_status_changed_at: datetime
    project_status_changed_by_id: int
    project_start_date: datetime
    project_expected_end_date: datetime
    project_approved_at: datetime
    project_real_end_date: datetime
    project_planned_budget: float
    project_approved_budget: float
    project_spent_budget: float
    project_final_budget: float
    project_completion_percentage: float
    project_approvers_count: int
    project_public: bool
    project_scope: str
    project_expected_benefits: str
    project_risks: str
    project_assumptions: str
    project_constraints: str
    project_milestones: str
    project_tasks: str 
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int
    deleted_at: datetime
    deleted_by: int
    active: bool
    
    model_config = ConfigDict(from_attributes=True)