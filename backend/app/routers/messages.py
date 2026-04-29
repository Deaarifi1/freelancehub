from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.message import Conversation, Message
from app.models.user import User, UserRole
from app.schemas.message import ConversationCreate, ConversationResponse, MessageCreate, MessageResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/conversations", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    conv_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Krijo konversacion të ri."""
    existing = db.query(Conversation).filter(
        Conversation.client_id == current_user.id,
        Conversation.freelancer_id == conv_data.freelancer_id,
        Conversation.project_id == conv_data.project_id
    ).first()
    if existing:
        return existing

    conversation = Conversation(
        client_id=current_user.id,
        freelancer_id=conv_data.freelancer_id,
        project_id=conv_data.project_id
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_my_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr të gjitha konversacionet e përdoruesit."""
    conversations = db.query(Conversation).filter(
        (Conversation.client_id == current_user.id) |
        (Conversation.freelancer_id == current_user.id)
    ).all()
    return conversations

@router.post("/", response_model=MessageResponse, status_code=201)
async def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Dërgo mesazh."""
    conversation = db.query(Conversation).filter(
        Conversation.id == message_data.conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Konversacioni nuk u gjet")

    if conversation.client_id != current_user.id and conversation.freelancer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    message = Message(
        conversation_id=message_data.conversation_id,
        sender_id=current_user.id,
        content=message_data.content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.get("/{conversation_id}", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr mesazhet e një konversacioni."""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Konversacioni nuk u gjet")

    if conversation.client_id != current_user.id and conversation.freelancer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()
    return messages

@router.put("/{conversation_id}/read", status_code=200)
async def mark_as_read(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Shëno mesazhet si të lexuara."""
    db.query(Message).filter(
        Message.conversation_id == conversation_id,
        Message.sender_id != current_user.id,
        Message.is_read == False
    ).update({"is_read": True})
    db.commit()
    return {"message": "Mesazhet u shënuan si të lexuara"}