from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ConversationCreate(BaseModel):
    freelancer_id: int
    project_id: Optional[int] = None

class ConversationResponse(BaseModel):
    id: int
    client_id: int
    freelancer_id: int
    project_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    conversation_id: int
    content: str

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True