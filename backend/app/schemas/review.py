from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    contract_id: int
    reviewee_id: int
    rating: float = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    contract_id: int
    reviewer_id: int
    reviewee_id: int
    rating: float
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True