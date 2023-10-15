from app.database import models, database


class CandidateRepository:
    async def create_candidate(self, new_candidate: dict) -> None:
        candidate = models.Candidate(**new_candidate)
        with database.create_session() as db:
            db.add(candidate)
            db.commit()

    async def get_soft_skill_by_name(self, name: str) -> models.SoftSkill:
        with database.create_session() as db:
            return db.query(models.SoftSkill).filter_by(name=name).first()

    async def get_tech_skill_by_name(self, name: str) -> models.Technology:
        with database.create_session() as db:
            return db.query(models.Technology).filter_by(name=name).first()
