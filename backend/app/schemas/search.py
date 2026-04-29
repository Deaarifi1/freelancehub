from pydantic import BaseModel
from typing import Optional

class FreelancerSearchResponse(BaseModel):
    id: int
    user_id: int
    bio: Optional[str]
    hourly_rate: Optional[float]
    experience_years: int
    average_rating: float
    is_available: bool

    class Config:
        from_attributes = True