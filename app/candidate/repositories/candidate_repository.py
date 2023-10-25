from sqlalchemy import func
from sqlalchemy.orm import joinedload
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

    async def get_candidates_filtered(self, tech_skills_ids=None, soft_skills_ids=None):
        with database.create_session() as db:
            query = db.query(models.Candidate)

            tech_skill_subquery = None
            soft_skill_subquery = None

            if tech_skills_ids:
                tech_skill_subquery = (
                    db.query(models.Candidate.user_id)
                    .join(models.Candidate.tech_skills)
                    .filter(models.Technology.id.in_(tech_skills_ids))
                    .group_by(models.Candidate.user_id)
                    .having(func.count(models.Technology.id) == len(tech_skills_ids))
                )

            if soft_skills_ids:
                soft_skill_subquery = (
                    db.query(models.Candidate.user_id)
                    .join(models.Candidate.soft_skills)
                    .filter(models.SoftSkill.id.in_(soft_skills_ids))
                    .group_by(models.Candidate.user_id)
                    .having(func.count(models.SoftSkill.id) == len(soft_skills_ids))
                )

            if tech_skill_subquery and soft_skill_subquery:
                common_candidates_subquery = tech_skill_subquery.intersect(
                    soft_skill_subquery
                )
                query = query.filter(
                    models.Candidate.user_id.in_(common_candidates_subquery)
                )
            elif tech_skill_subquery:
                query = query.filter(models.Candidate.user_id.in_(tech_skill_subquery))
            elif soft_skill_subquery:
                query = query.filter(models.Candidate.user_id.in_(soft_skill_subquery))

            candidates_with_skills = query.options(
                joinedload(models.Candidate.soft_skills),
                joinedload(models.Candidate.tech_skills),
            ).all()

            return candidates_with_skills
