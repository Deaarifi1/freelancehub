from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.bid import Bid, BidStatus
from app.models.project import Project
from app.models.freelancer import FreelancerProfile
from app.models.user import User, UserRole
from app.schemas.bid import BidCreate, BidUpdate, BidResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/bids", tags=["Bids"])

@router.post("/", response_model=BidResponse, status_code=201)
async def create_bid(
    bid_data: BidCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Freelancer dërgon ofertë për projekt."""
    if current_user.role != UserRole.FREELANCER:
        raise HTTPException(
            status_code=403,
            detail="Vetëm freelancerët mund të dërgojnë oferta"
        )

    project = db.query(Project).filter(Project.id == bid_data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projekti nuk u gjet")

    freelancer = db.query(FreelancerProfile).filter(
        FreelancerProfile.user_id == current_user.id
    ).first()
    if not freelancer:
        raise HTTPException(status_code=404, detail="Profili i freelancerit nuk u gjet")

    existing_bid = db.query(Bid).filter(
        Bid.project_id == bid_data.project_id,
        Bid.freelancer_id == freelancer.id
    ).first()
    if existing_bid:
        raise HTTPException(status_code=400, detail="Keni dërguar tashmë ofertë për këtë projekt")

    bid = Bid(
        project_id=bid_data.project_id,
        freelancer_id=freelancer.id,
        amount=bid_data.amount,
        proposal=bid_data.proposal,
        delivery_days=bid_data.delivery_days
    )
    db.add(bid)
    db.commit()
    db.refresh(bid)
    return bid

@router.get("/project/{project_id}", response_model=List[BidResponse])
async def get_project_bids(project_id: int, db: Session = Depends(get_db)):
    """Merr të gjitha ofertat për një projekt."""
    bids = db.query(Bid).filter(Bid.project_id == project_id).all()
    return bids

@router.get("/my-bids", response_model=List[BidResponse])
async def get_my_bids(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Freelancer sheh ofertat e tij."""
    freelancer = db.query(FreelancerProfile).filter(
        FreelancerProfile.user_id == current_user.id
    ).first()
    if not freelancer:
        raise HTTPException(status_code=404, detail="Profili nuk u gjet")

    bids = db.query(Bid).filter(Bid.freelancer_id == freelancer.id).all()
    return bids

@router.put("/{bid_id}/accept", response_model=BidResponse)
async def accept_bid(
    bid_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Klienti pranon ofertën."""
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Oferta nuk u gjet")

    project = db.query(Project).filter(Project.id == bid.project_id).first()
    if project.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    bid.status = BidStatus.ACCEPTED
    db.commit()
    db.refresh(bid)
    return bid

@router.put("/{bid_id}/reject", response_model=BidResponse)
async def reject_bid(
    bid_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Klienti refuzon ofertën."""
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Oferta nuk u gjet")

    project = db.query(Project).filter(Project.id == bid.project_id).first()
    if project.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    bid.status = BidStatus.REJECTED
    db.commit()
    db.refresh(bid)
    return bid

@router.delete("/{bid_id}", status_code=204)
async def delete_bid(
    bid_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Freelancer tërheq ofertën."""
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Oferta nuk u gjet")

    freelancer = db.query(FreelancerProfile).filter(
        FreelancerProfile.user_id == current_user.id
    ).first()
    if bid.freelancer_id != freelancer.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    db.delete(bid)
    db.commit()