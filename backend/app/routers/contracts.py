from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.contract import Contract, ContractStatus
from app.models.bid import Bid, BidStatus
from app.models.project import Project, ProjectStatus
from app.models.milestone import Milestone
from app.models.freelancer import FreelancerProfile
from app.models.user import User
from app.schemas.contract import ContractCreate, ContractResponse, MilestoneCreate, MilestoneResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.post("/", response_model=ContractResponse, status_code=201)
async def create_contract(
    contract_data: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Klienti krijon kontratë pasi pranon ofertën."""
    bid = db.query(Bid).filter(Bid.id == contract_data.bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Oferta nuk u gjet")

    project = db.query(Project).filter(Project.id == contract_data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projekti nuk u gjet")

    if project.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    bid.status = BidStatus.ACCEPTED
    project.status = ProjectStatus.IN_PROGRESS

    contract = Contract(
        project_id=contract_data.project_id,
        bid_id=contract_data.bid_id,
        client_id=current_user.id,
        freelancer_id=bid.freelancer_id,
        total_amount=bid.amount,
        terms=contract_data.terms
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract

@router.get("/", response_model=List[ContractResponse])
async def get_my_contracts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr kontratat e përdoruesit aktual."""
    contracts = db.query(Contract).filter(
        (Contract.client_id == current_user.id) |
        (Contract.freelancer_id == current_user.id)
    ).all()
    return contracts

@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr kontratën sipas ID."""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Kontrata nuk u gjet")
    if contract.client_id != current_user.id and contract.freelancer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")
    return contract

@router.put("/{contract_id}/complete", response_model=ContractResponse)
async def complete_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Klienti mbyll kontratën si të përfunduar."""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Kontrata nuk u gjet")
    if contract.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    contract.status = ContractStatus.COMPLETED
    project = db.query(Project).filter(Project.id == contract.project_id).first()
    project.status = ProjectStatus.COMPLETED
    db.commit()
    db.refresh(contract)
    return contract

@router.post("/{contract_id}/milestones", response_model=MilestoneResponse, status_code=201)
async def create_milestone(
    contract_id: int,
    milestone_data: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Shto milestone në kontratë."""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Kontrata nuk u gjet")
    if contract.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    milestone = Milestone(
        contract_id=contract_id,
        **milestone_data.model_dump()
    )
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    return milestone

@router.get("/{contract_id}/milestones", response_model=List[MilestoneResponse])
async def get_milestones(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr milestones e kontratës."""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Kontrata nuk u gjet")

    milestones = db.query(Milestone).filter(
        Milestone.contract_id == contract_id
    ).all()
    return milestones

@router.put("/{contract_id}/milestones/{milestone_id}/complete", response_model=MilestoneResponse)
async def complete_milestone(
    contract_id: int,
    milestone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Shëno milestone si të përfunduar."""
    milestone = db.query(Milestone).filter(
        Milestone.id == milestone_id,
        Milestone.contract_id == contract_id
    ).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone nuk u gjet")

    milestone.is_completed = True
    db.commit()
    db.refresh(milestone)
    return milestone