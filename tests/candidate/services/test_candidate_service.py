import pytest
from unittest.mock import Mock, AsyncMock

from app.database.schemas import CreateCandidate
from app.candidate.services.candidate_service import CandidateService


class TestCandidateService:
    @pytest.mark.asyncio
    async def test_create_candidate(self):
        mocked_repository = Mock()

        mocked_tech_skill = Mock(id=1, name="NodeJS")
        mocked_repository.get_tech_skill_by_name = AsyncMock()
        mocked_repository.get_tech_skill_by_name.return_value = mocked_tech_skill

        mocked_soft_skill = Mock(id=1, name="Responsibility")
        mocked_repository.get_soft_skill_by_name = AsyncMock()
        mocked_repository.get_soft_skill_by_name.return_value = mocked_soft_skill

        mocked_repository.create_candidate = AsyncMock()

        service = CandidateService(mocked_repository)

        new_candidate = CreateCandidate(
            user_id=1,
            fullname="John Doe",
            tech_skills=["NodeJS"],
            soft_skills=["Responsibility"],
        )

        await service.create_candidate(new_candidate)

        mocked_repository.create_candidate.assert_called_once_with(
            {
                "user_id": new_candidate.user_id,
                "fullname": new_candidate.fullname,
                "soft_skills": [mocked_soft_skill],
                "tech_skills": [mocked_tech_skill],
            }
        )

    @pytest.mark.asyncio
    async def test_get_candidates_paginated(self):
        mocked_repository = Mock()
        mocked_repository.get_candidates_filtered = AsyncMock()
        mocked_repository.get_candidates_filtered.return_value = {
            "data": [],
            "total_pages": 1,
        }

        service = CandidateService(mocked_repository)

        response = await service.get_candidates_paginated(
            page=1,
            limit=10,
            tech_skills=["NodeJS"],
            soft_skills=["Responsibility"],
            id_list=["1,2"],
        )

        assert "data" in response
        assert "total_pages" in response
