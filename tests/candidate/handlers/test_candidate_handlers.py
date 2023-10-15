import json
import pytest
from unittest.mock import Mock, AsyncMock
from app.candidate.handlers.candidate_handlers import create_candidate_handler


class TestCandidateHandler:
    @pytest.mark.asyncio
    async def test_create_candidate_handler(self):
        mocked_service = Mock()
        mocked_service.create_candidate = AsyncMock()

        handler = await create_candidate_handler(mocked_service)

        mocked_candidate = {
            "user_id": 1,
            "fullname": "John Doe",
            "soft_skills": ["Responsibility"],
            "tech_skills": ["ReactJS"],
        }

        message_mock = json.dumps(mocked_candidate).encode("utf-8")

        await handler(message_mock)

        assert mocked_service.create_candidate.call_count == 1
