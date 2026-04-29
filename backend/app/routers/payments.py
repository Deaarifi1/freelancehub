from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.database import get_db
from app.models.payment import Payment, PaymentStatus, EscrowAccount
from app.models.contract import Contract, ContractStatus
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentResponse, EscrowResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse, status_code=201)
async def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Klienti bën pagesë për kontratën."""
    contract = db.query(Contract).filter(
        Contract.id == payment_data.contract_id
    ).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Kontrata nuk u gjet")
    if contract.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    payment = Payment(
        contract_id=payment_data.contract_id,
        amount=payment_data.amount,
        status=PaymentStatus.COMPLETED,
        transaction_id=str(uuid.uuid4())
    )
    db.add(payment)

    # Shto në escrow
    escrow = db.query(EscrowAccount).filter(
        EscrowAccount.contract_id == payment_data.contract_id
    ).first()
    if escrow:
        escrow.balance += payment_data.amount
    else:
        escrow = EscrowAccount(
            contract_id=payment_data.contract_id,
            balance=payment_data.amount
        )
        db.add(escrow)

    db.commit()
    db.refresh(payment)
    return payment

@router.get("/contract/{contract_id}", response_model=List[PaymentResponse])
async def get_contract_payments(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr pagesat e një kontrate."""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Kontrata nuk u gjet")
    if contract.client_id != current_user.id and contract.freelancer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    payments = db.query(Payment).filter(
        Payment.contract_id == contract_id
    ).all()
    return payments

@router.get("/escrow/{contract_id}", response_model=EscrowResponse)
async def get_escrow(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr gjendjen e escrow për kontratën."""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Kontrata nuk u gjet")
    if contract.client_id != current_user.id and contract.freelancer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    escrow = db.query(EscrowAccount).filter(
        EscrowAccount.contract_id == contract_id
    ).first()
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow nuk u gjet")
    return escrow

@router.put("/escrow/{contract_id}/release", response_model=EscrowResponse)
async def release_escrow(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Klienti liron escrow-n — pagesa shkon te freelanceri."""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Kontrata nuk u gjet")
    if contract.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    escrow = db.query(EscrowAccount).filter(
        EscrowAccount.contract_id == contract_id
    ).first()
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow nuk u gjet")
    if escrow.is_released:
        raise HTTPException(status_code=400, detail="Escrow është liruar tashmë")

    escrow.is_released = True
    db.commit()
    db.refresh(escrow)
    return escrow

@router.get("/my-payments", response_model=List[PaymentResponse])
async def get_my_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr të gjitha pagesat e përdoruesit."""
    contracts = db.query(Contract).filter(
        (Contract.client_id == current_user.id) |
        (Contract.freelancer_id == current_user.id)
    ).all()

    contract_ids = [c.id for c in contracts]
    payments = db.query(Payment).filter(
        Payment.contract_id.in_(contract_ids)
    ).all()
    return payments