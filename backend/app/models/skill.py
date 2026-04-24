from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Relationships
    category = relationship("Category", back_populates="skills")
    freelancer_skills = relationship("FreelancerSkill", back_populates="skill")
    project_skills = relationship("ProjectSkill", back_populates="skill")

class FreelancerSkill(Base):
    __tablename__ = "freelancer_skills"

    id = Column(Integer, primary_key=True, index=True)
    freelancer_id = Column(Integer, ForeignKey("freelancer_profiles.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    level = Column(String(20), default="intermediate")

    # Relationships
    freelancer = relationship("FreelancerProfile", back_populates="skills")
    skill = relationship("Skill", back_populates="freelancer_skills")

class ProjectSkill(Base):
    __tablename__ = "project_skills"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="required_skills")
    skill = relationship("Skill", back_populates="project_skills")