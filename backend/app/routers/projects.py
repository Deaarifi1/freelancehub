from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.project import Project, ProjectStatus
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.dependencies import get_current_user, require_client
from app.cache import cache

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new project"""
    project = Project(
        **project_data.model_dump(),
        client_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Clear the list cache
    cache.delete_pattern("projects:list")
    return project

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 20,
    status: Optional[ProjectStatus] = None,
    db: Session = Depends(get_db)
):
    """ Get all the projects -  Redis cache """
    cache_key = f"projects:list:{skip}:{limit}:{status}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    query = db.query(Project)
    if status:
        query = query.filter(Project.status == status)
    projects = query.offset(skip).limit(limit).all()

    # save in cache for 5 minutes
    result = [ProjectResponse.model_validate(p).model_dump() for p in projects]
    cache.set(cache_key, result, expire=300)
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int, 
    db: Session = Depends(get_db)
    ):

    """ get project by ID - with redis cache """
    cache_key = f"projects:{project_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # save project for 10 minutes
    cache.set(cache_key, ProjectResponse.model_validate(project).model_dump(), expire=600)
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """update project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="project not found")
    if project.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have premission")

    for key, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    #delete cache
    cache.delete(f"projects:{project_id}")
    cache.delete_pattern("projects:list")
    return project

@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    """delete the project """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have premission")

    db.delete(project)
    db.commit()

    # delete cache
    cache.delete(f"projects:{project_id}")
    cache.delete_pattern("projects:list")