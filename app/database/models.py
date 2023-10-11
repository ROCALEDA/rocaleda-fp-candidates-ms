from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Candidate(Base):
    __tablename__ = "candidate"

    user_id = Column(Integer, primary_key=True)
    fullname = Column(String)

    tech_skills = relationship("Technology", secondary="candidate_tech_skill")
    soft_skills = relationship("SoftSkill", secondary="candidate_soft_skill")


class Technology(Base):
    __tablename__ = "technology"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    candidates = relationship("Candidate", secondary="candidate_tech_skill")


class CandidateTechSkill(Base):
    __tablename__ = "candidate_tech_skill"

    candidate_id = Column(Integer, ForeignKey("candidate.user_id"), primary_key=True)
    technology_id = Column(Integer, ForeignKey("technology.id"), primary_key=True)


class SoftSkill(Base):
    __tablename__ = "soft_skill"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    candidates = relationship("Candidate", secondary="candidate_soft_skill")


class CandidateSoftSkill(Base):
    __tablename__ = "candidate_soft_skill"

    candidate_id = Column(Integer, ForeignKey("candidate.user_id"), primary_key=True)
    soft_skill_id = Column(Integer, ForeignKey("soft_skill.id"), primary_key=True)
