from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class FreelancerProfile(Base):
    __tablename__ = "freelancer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    hourly_rate = Column(Float, nullable=True)
    experience_years = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="freelancer_profile")
    skills = relationship("FreelancerSkill", back_populates="freelancer")
    bids = relationship("Bid", back_populates="freelancer")
    portfolio = relationship("Portfolio", back_populates="freelancer")
    ai_matches = relationship("AIMatch", back_populates="freelancer")