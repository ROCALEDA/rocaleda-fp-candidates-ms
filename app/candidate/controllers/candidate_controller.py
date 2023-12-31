import base64
import json
from fastapi import APIRouter, Body, HTTPException, Query
from app.database.schemas import PubSubMessage, CreateCandidate
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.candidate.services.candidate_service import CandidateService


router = APIRouter(
    prefix="/candidates",
    tags=["candidates"],
    responses={404: {"description": "Not found"}},
)


def initialize(candidate_service: "CandidateService"):
    @router.post("/push")
    async def create_candidate_from_push(data: PubSubMessage = Body(...)):
        message = data.message
        if not message:
            raise HTTPException(status_code=400, detail="Invalid message format")
        decoded_data = base64.b64decode(message["data"]).decode("utf-8")
        data_dict = json.loads(decoded_data)

        print("Received message from pubsub: ", data_dict)
        candidate = CreateCandidate(**data_dict)
        await candidate_service.create_candidate(candidate)

        return {"success": True}

    @router.get("")
    async def get_candidates_paginated(
        tech_skills: str = Query(None),
        soft_skills: str = Query(None),
        ids: str = Query(None),
        page: int = Query(1),
        limit: int = Query(10),
    ):
        tech_list = tech_skills.split(",") if tech_skills else []
        soft_list = soft_skills.split(",") if soft_skills else []
        id_list = ids.split(",") if ids else []

        return await candidate_service.get_candidates_paginated(
            tech_skills=tech_list,
            soft_skills=soft_list,
            id_list=id_list,
            page=page,
            limit=limit,
        )

    return {
        "create_candidate_from_push": create_candidate_from_push,
        "get_candidates_paginated": get_candidates_paginated,
    }
