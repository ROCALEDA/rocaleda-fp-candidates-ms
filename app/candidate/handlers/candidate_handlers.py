from typing import Any
from app.database.schemas import CreateCandidate
from app.candidate.services.candidate_service import CandidateService


async def create_candidate_handler(service: CandidateService):
    async def handler(message: Any) -> None:
        parsed_message = message.decode("utf-8")
        parsed_message = CreateCandidate.model_validate(parsed_message)
        await service.create_candidate(parsed_message)

    return handler
