from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.project import ProjectStatus, ProjectType

class ProjectCreate(BaseModel):
    title: str
    description: str
    budget_min: float
    budget_max: float
    project_type: ProjectType = ProjectType.FIXED
    deadline: Optional[datetime] = None
    category_id: Optional[int] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    status: Optional[ProjectStatus] = None

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    budget_min: float
    budget_max: float
    status: ProjectStatus
    project_type: ProjectType
    client_id: int
    created_at: datetime

    class Config:
        from_attributes = True