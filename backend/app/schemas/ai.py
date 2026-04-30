from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AIMatchResponse(BaseModel):
    id: int
    project_id: int
    freelancer_id: int
    score: float
    reason: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectAnalysisRequest(BaseModel):
    description: str

class ProjectAnalysisResponse(BaseModel):
    skills: list
    budget_range: dict
    complexity: str
    estimated_duration: str