from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import Token, UserCreate, UserResponse
from app.dependencies import get_current_user
from app.models.user import User
from app.tasks.email_tasks import send_welcome_email

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """New user registration"""
    user = await auth_service.register(user_data, db)

    # send email in the background
    send_welcome_email.delay(user.email, user.username)
    
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login dhe marrja e JWT token."""
    return await auth_service.login(form_data.username, form_data.password, db)

@router.post("/refresh", response_model=Token)
async def refresh_token(token: str, db: Session = Depends(get_db)):
    """Rifresko JWT token."""
    return await auth_service.refresh_token(token)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Merr të dhënat e përdoruesit aktual."""
    return current_user