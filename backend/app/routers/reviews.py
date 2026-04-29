from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.review import Review
from app.models.contract import Contract, ContractStatus
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse, status_code=201)
async def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Krijo review pas përfundimit të kontratës."""
    contract = db.query(Contract).filter(
        Contract.id == review_data.contract_id
    ).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Kontrata nuk u gjet")

    if contract.client_id != current_user.id and contract.freelancer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nuk keni leje")

    if contract.status != ContractStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Mund të lini review vetëm për kontrata të përfunduara"
        )

    existing = db.query(Review).filter(
        Review.contract_id == review_data.contract_id,
        Review.reviewer_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Keni lënë tashmë review për këtë kontratë"
        )

    review = Review(
        contract_id=review_data.contract_id,
        reviewer_id=current_user.id,
        reviewee_id=review_data.reviewee_id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("/user/{user_id}", response_model=List[ReviewResponse])
async def get_user_reviews(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Merr të gjitha reviews për një përdorues."""
    reviews = db.query(Review).filter(
        Review.reviewee_id == user_id
    ).all()
    return reviews

@router.get("/contract/{contract_id}", response_model=List[ReviewResponse])
async def get_contract_reviews(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """Merr reviews për një kontratë."""
    reviews = db.query(Review).filter(
        Review.contract_id == contract_id
    ).all()
    return reviews

@router.get("/my-reviews", response_model=List[ReviewResponse])
async def get_my_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Merr reviews e marra nga përdoruesi aktual."""
    reviews = db.query(Review).filter(
        Review.reviewee_id == current_user.id
    ).all()
    return reviews