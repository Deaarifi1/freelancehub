from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AgencyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None

class AgencyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    is_active: Optional[bool] = None

class AgencyResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    website: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True