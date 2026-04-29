from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.contract import ContractStatus

class ContractCreate(BaseModel):
    project_id: int
    bid_id: int
    terms: Optional[str] = None

class ContractResponse(BaseModel):
    id: int
    project_id: int
    bid_id: int
    client_id: int
    freelancer_id: int
    total_amount: float
    status: ContractStatus
    terms: Optional[str]
    start_date: datetime
    end_date: Optional[datetime]

    class Config:
        from_attributes = True

class MilestoneCreate(BaseModel):
    title: str
    description: Optional[str] = None
    amount: float
    due_date: Optional[datetime] = None

class MilestoneResponse(BaseModel):
    id: int
    contract_id: int
    title: str
    description: Optional[str]
    amount: float
    is_completed: bool
    due_date: Optional[datetime]

    class Config:
        from_attributes = True