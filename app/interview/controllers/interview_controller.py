from fastapi import APIRouter, Header, Query
from typing import TYPE_CHECKING

from app.database.schemas import InterviewsResponse

if TYPE_CHECKING:
    from app.interview.services.interview_service import InterviewService

router = APIRouter(
    prefix="/interviews",
    tags=["interviews"],
    responses={404: {"description": "Not found"}},
)


def initialize(interview_service: "InterviewService"):
    @router.get("")
    async def get_interviews_paginated(
        role: int = Header(...),
        user_id: int = Query(...),
        page: int = Query(1),
        limit: int = Query(10),
    ) -> InterviewsResponse:
        return await interview_service.get_interviews_paginated(
            role=role,
            user_id=user_id,
            page=page,
            limit=limit,
        )

    return {
        "get_interviews_paginated": get_interviews_paginated,
    }
