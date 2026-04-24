from sqlalchemy import Column, Integer, Text, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class ContractStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), unique=True, nullable=False)
    bid_id = Column(Integer, ForeignKey("bids.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    freelancer_id = Column(Integer, ForeignKey("freelancer_profiles.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(ContractStatus), default=ContractStatus.ACTIVE)
    terms = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="contract")
    bid = relationship("Bid")
    milestones = relationship("Milestone", back_populates="contract")
    payments = relationship("Payment", back_populates="contract")