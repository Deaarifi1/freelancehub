from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.bid import BidStatus

class BidCreate(BaseModel):
    project_id: int
    amount: float
    proposal: str
    delivery_days: int

class BidUpdate(BaseModel):
    amount: Optional[float] = None
    proposal: Optional[str] = None
    delivery_days: Optional[int] = None

class BidResponse(BaseModel):
    id: int
    project_id: int
    freelancer_id: int
    amount: float
    proposal: str
    delivery_days: int
    status: BidStatus
    created_at: datetime

    class Config:
        from_attributes = True