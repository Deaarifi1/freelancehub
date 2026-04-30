from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.freelancer import FreelancerProfile
from app.models.portfolio import Portfolio
from app.schemas.user import UserResponse, UserUpdate, FreelancerProfileUpdate, FreelancerProfileResponse
from app.dependencies import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Merr të gjithë përdoruesit — vetëm Admin."""
    return db.query(User).offset(skip).limit(limit).all()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Merr përdoruesin sipas ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Përdoruesi nuk u gjet")
    return user

@router.put("/me", response_model=UserResponse)
async def update_me(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Përditëso të dhënat e përdoruesit aktual."""
    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me/profile", response_model=FreelancerProfileResponse)
async def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr profilin e freelancerit aktual."""
    profile = db.query(FreelancerProfile).filter(
        FreelancerProfile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profili nuk u gjet")
    return profile

@router.put("/me/profile", response_model=FreelancerProfileResponse)
async def update_my_profile(
    profile_data: FreelancerProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Përditëso profilin e freelancerit."""
    profile = db.query(FreelancerProfile).filter(
        FreelancerProfile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profili nuk u gjet")

    for key, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Fshi përdoruesin — vetëm Admin."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Përdoruesi nuk u gjet")
    db.delete(user)
    db.commit()