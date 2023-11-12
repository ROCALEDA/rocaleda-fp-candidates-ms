from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


# Item base de candidato
class CandidateBase(BaseModel):
    user_id: int
    fullname: str


# Item de detalle de candidato
class CreateCandidate(CandidateBase):
    tech_skills: List[str]
    soft_skills: List[str]


# Item para recepción de mensajes push PubSub
class PubSubMessage(BaseModel):
    message: dict


# Item base de entrevista
class InterviewBase(BaseModel):
    customer_id: int
    candidate_id: int
    realization_date: datetime
    open_position_id: Optional[int]
    score: Optional[int]
    result: Optional[str]


# Item con datos de entrevista respuesta
class InterviewResponseData(InterviewBase):
    id: int


# Respuesta servicio consulta de detalle de candidatos
class InterviewsResponse(BaseModel):
    data: List[InterviewResponseData]
    total_pages: int
