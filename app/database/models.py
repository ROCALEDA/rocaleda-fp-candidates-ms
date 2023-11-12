from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from .database import Base


class Candidate(Base):
    __tablename__ = "candidate"

    user_id = Column(Integer, primary_key=True)
    fullname = Column(String)

    # children relationships
    interviews = relationship("Interview", back_populates="candidate")
    tech_skills = relationship("Technology", secondary="candidate_tech_skill")
    soft_skills = relationship("SoftSkill", secondary="candidate_soft_skill")


class Technology(Base):
    __tablename__ = "technology"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    # children relationships
    candidates = relationship(
        "Candidate", secondary="candidate_tech_skill", back_populates="tech_skills"
    )


class CandidateTechSkill(Base):
    __tablename__ = "candidate_tech_skill"

    # related parent tables
    candidate_id = Column(Integer, ForeignKey("candidate.user_id"), primary_key=True)
    technology_id = Column(Integer, ForeignKey("technology.id"), primary_key=True)


class SoftSkill(Base):
    __tablename__ = "soft_skill"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    # children relationships
    candidates = relationship(
        "Candidate", secondary="candidate_soft_skill", back_populates="soft_skills"
    )


class CandidateSoftSkill(Base):
    __tablename__ = "candidate_soft_skill"

    # related parent tables
    candidate_id = Column(Integer, ForeignKey("candidate.user_id"), primary_key=True)
    soft_skill_id = Column(Integer, ForeignKey("soft_skill.id"), primary_key=True)


class Interview(Base):
    __tablename__ = "interview"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer)
    candidate_id = Column(Integer, ForeignKey("candidate.user_id"))
    realization_date = Column(DateTime)
    open_position_id = Column(Integer, nullable=True)
    score = Column(Numeric(5, 2), nullable=True)
    result = Column(String(20), nullable=True)

    # parents relationships
    candidate = relationship("Candidate", back_populates="interviews")
