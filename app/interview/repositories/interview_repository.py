from app.database import models, database


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
