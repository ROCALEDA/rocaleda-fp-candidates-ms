from typing import List
from pydantic import BaseModel


class CandidateBase(BaseModel):
    user_id: int
    fullname: str


class CreateCandidate(CandidateBase):
    tech_skills: List[str]
    soft_skills: List[str]


class PubSubMessage(BaseModel):
    message: dict
