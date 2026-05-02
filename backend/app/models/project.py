from sqlalchemy import Column, Integer, String, Text, Float, Enum, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class ProjectStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ProjectType(str, enum.Enum):
    FIXED = "fixed"
    HOURLY = "hourly"

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    budget_min = Column(Float, nullable=False)
    budget_max = Column(Float, nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.OPEN)
    project_type = Column(Enum(ProjectType), default=ProjectType.FIXED)
    deadline = Column(DateTime, nullable=True)
    
    # AI embedding for matching
    ai_embedding = Column(JSON, nullable=True)
    
    # Foreign Keys
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=True)  # Multi-tenancy
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    client = relationship("User", foreign_keys=[client_id])
    agency = relationship("Agency", back_populates="projects")
    category = relationship("Category", back_populates="projects")
    bids = relationship("Bid", back_populates="project")
    contract = relationship("Contract", back_populates="project", uselist=False)
    required_skills = relationship("ProjectSkill", back_populates="project")
    ai_matches = relationship("AIMatch", back_populates="project")