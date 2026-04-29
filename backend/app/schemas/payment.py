from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.payment import PaymentStatus

class PaymentCreate(BaseModel):
    contract_id: int
    amount: float

class PaymentResponse(BaseModel):
    id: int
    contract_id: int
    amount: float
    status: PaymentStatus
    transaction_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class EscrowResponse(BaseModel):
    id: int
    contract_id: int
    balance: float
    is_released: bool
    created_at: datetime

    class Config:
        from_attributes = True