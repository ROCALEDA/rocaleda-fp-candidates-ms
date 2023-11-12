from fastapi import HTTPException
from typing import TYPE_CHECKING

from app.database.schemas import InterviewsResponse

if TYPE_CHECKING:
    from app.interview.repositories.interview_repository import InterviewRepository


class InterviewService:
    def __init__(self, interview_repository: "InterviewRepository"):
        self.interview_repository = interview_repository

    async def get_interviews_paginated(
        self,
        role: int,
        user_id: int,
        page: int,
        limit: int,
    ) -> InterviewsResponse:
        if role == 2:
            return await self.interview_repository.get_customer_interviews(
                user_id, page, limit
            )
        if role == 3:
            return await self.interview_repository.get_candidate_interviews(
                user_id, page, limit
            )
        else:
            raise HTTPException(403)
