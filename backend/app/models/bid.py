from sqlalchemy import Column, Integer, Text, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class BidStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    freelancer_id = Column(Integer, ForeignKey("freelancer_profiles.id"), nullable=False)
    amount = Column(Float, nullable=False)
    proposal = Column(Text, nullable=False)
    delivery_days = Column(Integer, nullable=False)
    status = Column(Enum(BidStatus), default=BidStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    project = relationship("Project", back_populates="bids")
    freelancer = relationship("FreelancerProfile", back_populates="bids")