import pytest
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock
from app.candidate.controllers import candidate_controller


class TestUserController:
    @pytest.mark.asyncio
    async def test_create_candidate_from_push(self):
        mock_service = Mock()
        mock_service.create_candidate = AsyncMock()

        data_mock = Mock(
            message={
                "user_id": 1,
                "fullname": "John Doe",
                "tech_skills": [],
                "soft_skills": [],
            }
        )

        create_candidate_func = candidate_controller.initialize(mock_service)[
            "create_candidate_from_push"
        ]

        response = await create_candidate_func(data_mock)

        assert "success" in response

    @pytest.mark.asyncio
    async def test_create_candidate_from_push_to_raise(self):
        mock_service = Mock()
        mock_service.create_candidate = AsyncMock()

        data_mock = Mock(message=None)

        create_candidate_func = candidate_controller.initialize(mock_service)[
            "create_candidate_from_push"
        ]

        with pytest.raises(HTTPException):
            await create_candidate_func(data_mock)
