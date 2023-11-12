import pytest
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock

from app.interview.services.interview_service import InterviewService


class TestPositionService:
    @pytest.mark.asyncio
    async def test_get_interviews_customer(self):
        mocked_repository = Mock()
        mocked_repository.get_customer_interviews = AsyncMock()

        interviews = [
            Mock(
                id=1,
                customer_id=21,
                candidate_id=31,
                subject="Entrevista técnica",
                realization_date="2021-02-03T08:30:00",
                score=88,
                open_position_id=22,
            ),
            Mock(
                id=2,
                customer_id=21,
                candidate_id=32,
                subject="Desconocido",
                realization_date="2021-02-03T09:30:00",
                score=None,
                open_position_id=None,
            ),
        ]
        customer_interviews = {
            "data": interviews,
            "total_pages": 1,
        }

        mocked_repository.get_customer_interviews.return_value = customer_interviews

        service = InterviewService(mocked_repository)

        role = 2
        customer_id = 21
        page = 1
        limit = 2

        func_response = await service.get_interviews_paginated(
            role, customer_id, page, limit
        )
        print(func_response)

        assert len(func_response["data"]) == 2
        assert func_response["data"][0].id == 1
        assert func_response["data"][0].customer_id == 21
        assert func_response["data"][0].candidate_id == 31
        assert func_response["data"][0].subject == "Entrevista técnica"
        assert func_response["data"][0].realization_date == "2021-02-03T08:30:00"
        assert func_response["data"][0].score == 88
        assert func_response["data"][0].open_position_id == 22

    @pytest.mark.asyncio
    async def test_get_interviews_candidate(self):
        mocked_repository = Mock()
        mocked_repository.get_candidate_interviews = AsyncMock()

        interviews = [
            Mock(
                id=1,
                customer_id=21,
                candidate_id=31,
                subject="Entrevista blanda",
                realization_date="2021-02-03T08:30:00",
                score=50,
                open_position_id=22,
            ),
            Mock(
                id=2,
                customer_id=22,
                candidate_id=31,
                subject="Desconocido",
                realization_date="2021-02-15T09:30:00",
                score=None,
                open_position_id=None,
            ),
        ]
        candidate_interviews = {
            "data": interviews,
            "total_pages": 1,
        }
        mocked_repository.get_candidate_interviews.return_value = candidate_interviews

        service = InterviewService(mocked_repository)

        role = 3
        candidate_id = 31
        page = 1
        limit = 2

        func_response = await service.get_interviews_paginated(
            role, candidate_id, page, limit
        )
        print(func_response)
        assert len(func_response["data"]) == 2
        assert func_response["data"][1].id == 2
        assert func_response["data"][1].customer_id == 22
        assert func_response["data"][1].candidate_id == 31
        assert func_response["data"][1].subject == "Desconocido"
        assert func_response["data"][1].realization_date == "2021-02-15T09:30:00"
        assert func_response["data"][1].score is None
        assert func_response["data"][1].open_position_id is None

    @pytest.mark.asyncio
    async def test_get_interviews_paginated_role_not_supported(self):
        mocked_repository = Mock()

        service = InterviewService(mocked_repository)

        role = 1
        user_id = 0
        page = 1
        limit = 2

        with pytest.raises(HTTPException) as exception_info:
            await service.get_interviews_paginated(role, user_id, page, limit)

        assert exception_info.value.status_code == 403
        assert exception_info.value.detail == "Forbidden"
