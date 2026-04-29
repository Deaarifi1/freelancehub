from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app.models.project import Project, ProjectStatus, ProjectType
from app.models.freelancer import FreelancerProfile
from app.models.user import User
from app.models.skill import Skill, FreelancerSkill
from app.schemas.project import ProjectResponse
from app.schemas.search import FreelancerSearchResponse

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/projects", response_model=List[ProjectResponse])
async def search_projects(
    q: Optional[str] = Query(None, description="Kërko sipas titullit ose përshkrimit"),
    status: Optional[ProjectStatus] = None,
    project_type: Optional[ProjectType] = None,
    budget_min: Optional[float] = None,
    budget_max: Optional[float] = None,
    category_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Kërko dhe filtro projektet."""
    query = db.query(Project)

    if q:
        query = query.filter(
            or_(
                Project.title.ilike(f"%{q}%"),
                Project.description.ilike(f"%{q}%")
            )
        )
    if status:
        query = query.filter(Project.status == status)
    if project_type:
        query = query.filter(Project.project_type == project_type)
    if budget_min:
        query = query.filter(Project.budget_min >= budget_min)
    if budget_max:
        query = query.filter(Project.budget_max <= budget_max)
    if category_id:
        query = query.filter(Project.category_id == category_id)

    return query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/freelancers", response_model=List[FreelancerSearchResponse])
async def search_freelancers(
    q: Optional[str] = Query(None, description="Kërko sipas bio"),
    skill: Optional[str] = None,
    min_rate: Optional[float] = None,
    max_rate: Optional[float] = None,
    min_rating: Optional[float] = None,
    is_available: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Kërko dhe filtro freelancerët."""
    query = db.query(FreelancerProfile)

    if q:
        query = query.join(User).filter(
            or_(
                FreelancerProfile.bio.ilike(f"%{q}%"),
                User.username.ilike(f"%{q}%")
            )
        )
    if skill:
        query = query.join(FreelancerSkill).join(Skill).filter(
            Skill.name.ilike(f"%{skill}%")
        )
    if min_rate:
        query = query.filter(FreelancerProfile.hourly_rate >= min_rate)
    if max_rate:
        query = query.filter(FreelancerProfile.hourly_rate <= max_rate)
    if min_rating:
        query = query.filter(FreelancerProfile.average_rating >= min_rating)
    if is_available is not None:
        query = query.filter(FreelancerProfile.is_available == is_available)

    return query.offset(skip).limit(limit).all()