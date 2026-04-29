from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.agency import Agency
from app.models.user import User, UserRole
from app.schemas.agency import AgencyCreate, AgencyUpdate, AgencyResponse
from app.dependencies import get_current_user, require_role

router = APIRouter(prefix="/agencies", tags=["Agencies"])

@router.post("/", response_model=AgencyResponse, status_code=201)
async def create_agency(
    agency_data: AgencyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN, UserRole.AGENCY_MANAGER)
    )
):
    """Krijo agjenci të re — tenant i ri."""
    existing = db.query(Agency).filter(
        Agency.name == agency_data.name
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Agjencia me këtë emër ekziston tashmë"
        )

    agency = Agency(**agency_data.model_dump())
    db.add(agency)
    db.commit()
    db.refresh(agency)

    # Lidh userin me agjencinë
    current_user.agency_id = agency.id
    db.commit()

    return agency

@router.get("/", response_model=List[AgencyResponse])
async def get_agencies(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Merr të gjitha agjencitë."""
    return db.query(Agency).filter(
        Agency.is_active == True
    ).offset(skip).limit(limit).all()

@router.get("/{agency_id}", response_model=AgencyResponse)
async def get_agency(
    agency_id: int,
    db: Session = Depends(get_db)
):
    """Merr agjencinë sipas ID."""
    agency = db.query(Agency).filter(Agency.id == agency_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Agjencia nuk u gjet")
    return agency

@router.put("/{agency_id}", response_model=AgencyResponse)
async def update_agency(
    agency_id: int,
    agency_data: AgencyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Përditëso agjencinë."""
    agency = db.query(Agency).filter(Agency.id == agency_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Agjencia nuk u gjet")

    if current_user.agency_id != agency_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    for key, value in agency_data.model_dump(exclude_unset=True).items():
        setattr(agency, key, value)

    db.commit()
    db.refresh(agency)
    return agency

@router.post("/{agency_id}/members/{user_id}", status_code=200)
async def add_member(
    agency_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Shto anëtar në agjenci — multi-tenancy."""
    agency = db.query(Agency).filter(Agency.id == agency_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Agjencia nuk u gjet")

    if current_user.agency_id != agency_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Përdoruesi nuk u gjet")

    user.agency_id = agency_id
    db.commit()
    return {"message": f"Përdoruesi u shtua në agjenci"}

@router.get("/{agency_id}/members", response_model=List[dict])
async def get_members(
    agency_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr anëtarët e agjencisë."""
    agency = db.query(Agency).filter(Agency.id == agency_id).first()
    if not agency:
        raise HTTPException(status_code=404, detail="Agjencia nuk u gjet")

    members = db.query(User).filter(User.agency_id == agency_id).all()
    return [
        {
            "id": m.id,
            "username": m.username,
            "email": m.email,
            "role": m.role
        }
        for m in members
    ]

@router.delete("/{agency_id}/members/{user_id}", status_code=200)
async def remove_member(
    agency_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Hiq anëtar nga agjencia."""
    if current_user.agency_id != agency_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Përdoruesi nuk u gjet")

    user.agency_id = None
    db.commit()
    return {"message": "Anëtari u hoq nga agjencia"}