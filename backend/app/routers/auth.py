from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Regjistrim i përdoruesit të ri."""
    return await auth_service.register(user_data, db)

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
    return await auth_service.refresh_token(token, db)

@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user = Depends(auth_service.get_current_user)):
    """Merr të dhënat e përdoruesit aktual."""
    return current_user