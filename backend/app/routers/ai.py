from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.project import Project
from app.models.freelancer import FreelancerProfile
from app.models.ai_match import AIMatch
from app.models.user import User
from app.services.ai_service import ai_service
from app.schemas.ai import AIMatchResponse, ProjectAnalysisRequest, ProjectAnalysisResponse
from app.dependencies import get_current_user
from app.tasks.ai_tasks import process_ai_matching

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/match/{project_id}", response_model=List[dict])
async def match_freelancers(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """AI gjen freelancerët më të mirë për projektin."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projekti nuk u gjet")

    if project.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    freelancers = db.query(FreelancerProfile).filter(
        FreelancerProfile.is_available == True
    ).all()

    if not freelancers:
        raise HTTPException(
            status_code=404,
            detail="Nuk ka freelancerë të disponueshëm"
        )

    matches = ai_service.match_freelancers(project, freelancers, db)
    return matches

@router.post("/analyze", response_model=ProjectAnalysisResponse)
async def analyze_project(
    request: ProjectAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """AI analizon projektin dhe sugjeron skill-e dhe budget."""
    result = ai_service.analyze_project(request.description)
    return result

@router.get("/matches/{project_id}", response_model=List[AIMatchResponse])
async def get_ai_matches(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr rezultatet e AI matching për projektin."""
    matches = db.query(AIMatch).filter(
        AIMatch.project_id == project_id
    ).order_by(AIMatch.score.desc()).all()
    return matches

@router.post("/match-background/{project_id}")
async def match_background(
    project_id: int,
    current_user: User = Depends(get_current_user)
):
    """Trigger AI matching në background me Celery."""
    task = process_ai_matching.delay(project_id)
    return {
        "message": "AI matching po procesohet në background",
        "task_id": task.id
    }

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Kontrollo statusin e Celery task-ut."""
    from app.tasks.celery_app import celery_app
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": str(task.result) if task.result else None
    }