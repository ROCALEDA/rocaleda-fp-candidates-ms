from app.database import models, database
from app.database.schemas import InterviewBase


class InterviewRepository:
    async def get_candidate_interviews(
        self, candidate_id: int, page: int, page_size: int
    ):
        with database.create_session() as db:
            query = (
                db.query(models.Interview)
                .filter_by(candidate_id=candidate_id)
                .order_by(models.Interview.realization_date)
            )
            total_count = query.count()
            total_pages = (total_count + page_size - 1) // page_size
            offset = (page - 1) * page_size
            query = query.offset(offset).limit(page_size)
            return {"data": query.all(), "total_pages": total_pages}

    async def get_customer_interviews(
        self, customer_id: int, page: int, page_size: int
    ):
        with database.create_session() as db:
            query = (
                db.query(models.Interview)
                .filter_by(customer_id=customer_id)
                .order_by(models.Interview.realization_date)
            )
            total_count = query.count()
            total_pages = (total_count + page_size - 1) // page_size
            offset = (page - 1) * page_size
            query = query.offset(offset).limit(page_size)
            return {"data": query.all(), "total_pages": total_pages}

    async def create_interview(self, interview: InterviewBase):
        with database.create_session() as db:
            new_interview = models.Interview(
                customer_id=interview.customer_id,
                candidate_id=interview.candidate_id,
                subject=interview.subject,
                realization_date=interview.realization_date,
                score=None,
                open_position_id=interview.open_position_id,
            )
            db.add(new_interview)
            db.commit()

            return new_interview
