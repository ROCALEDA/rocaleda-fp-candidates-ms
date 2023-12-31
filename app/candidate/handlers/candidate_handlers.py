import json
from typing import Any
from typing import TYPE_CHECKING
from app.database.schemas import CreateCandidate

if TYPE_CHECKING:
    from app.candidate.services.candidate_service import CandidateService


async def create_candidate_handler(service: "CandidateService"):
    async def handler(message: Any) -> None:
        parsed_message = json.loads(message.decode("utf-8"))
        print(f"Processing message {(parsed_message)}")
        parsed_message = CreateCandidate.model_validate(parsed_message)
        await service.create_candidate(parsed_message)

    return handler
