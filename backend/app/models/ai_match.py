from sqlalchemy import Column, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class AIMatch(Base):
    __tablename__ = "ai_matches"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    freelancer_id = Column(Integer, ForeignKey("freelancer_profiles.id"), nullable=False)
    score = Column(Float, nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    project = relationship("Project", back_populates="ai_matches")
    freelancer = relationship("FreelancerProfile", back_populates="ai_matches")