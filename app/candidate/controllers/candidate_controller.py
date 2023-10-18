import base64
import json
from fastapi import APIRouter, Body, HTTPException
from app.database.schemas import PubSubMessage, CreateCandidate
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.candidate.services.candidate_service import CandidateService


router = APIRouter(
    prefix="/candidate",
    tags=["candidate"],
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

    return {
        "create_candidate_from_push": create_candidate_from_push,
    }
