import pytest
from unittest.mock import Mock, AsyncMock

from app.interview.controllers import interview_controller


class TestInterviewController:
    @pytest.mark.asyncio
    async def test_get_interviews_paginated(self):
        mocked_service = Mock()
        mocked_service.get_interviews_paginated = AsyncMock()

        interviews_data = {
            "data": [
                {
                    "id": 1,
                    "customer_id": 21,
                    "candidate_id": 31,
                    "realization_date": "2021-02-03T08:30:00",
                    "open_position_id": 22,
                    "score": 88,
                    "result": "Satisfactorio",
                },
                {
                    "id": 2,
                    "customer_id": 21,
                    "candidate_id": 32,
                    "realization_date": "2021-02-03T09:30:00",
                    "open_position_id": 22,
                    "score": None,
                    "result": None,
                },
            ],
            "total_pages": 1,
        }

        mocked_service.get_interviews_paginated.return_value = interviews_data

        user_id = 21
        page = 1
        limit = 2
        role = 2

        get_interviews_paginated_func = interview_controller.initialize(mocked_service)[
            "get_interviews_paginated"
        ]

        func_response = await get_interviews_paginated_func(role, user_id, page, limit)

        mocked_service.get_interviews_paginated.assert_called_once_with(
            role=role, user_id=user_id, page=page, limit=limit
        )
        assert func_response == interviews_data
