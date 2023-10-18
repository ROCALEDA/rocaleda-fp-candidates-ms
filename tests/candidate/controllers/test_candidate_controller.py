import pytest
import json
import base64
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock
from app.candidate.controllers import candidate_controller


class TestUserController:
    @pytest.mark.asyncio
    async def test_create_candidate_from_push(self):
        mock_service = Mock()
        mock_service.create_candidate = AsyncMock()

        data_to_encode = {
            "user_id": 1,
            "fullname": "John Doe",
            "tech_skills": [],
            "soft_skills": [],
        }
        json_str = json.dumps(data_to_encode)
        encoded_data = base64.b64encode(json_str.encode("utf-8"))

        data_mock = Mock(message={"data": encoded_data})

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
