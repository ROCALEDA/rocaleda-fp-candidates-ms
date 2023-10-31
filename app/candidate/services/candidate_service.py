from typing import TYPE_CHECKING
from app.commons.enums import SoftSkill, TechSkill

from app.database.schemas import CreateCandidate

if TYPE_CHECKING:
    from app.candidate.repositories.candidate_repository import CandidateRepository


class CandidateService:
    def __init__(self, candidate_repository: "CandidateRepository"):
        self.candidate_repository = candidate_repository

    async def create_candidate(self, new_candidate: CreateCandidate) -> None:
        tech_skill_objects = [
            await self.candidate_repository.get_tech_skill_by_name(skill)
            for skill in new_candidate.tech_skills
        ]

        soft_skill_objects = [
            await self.candidate_repository.get_soft_skill_by_name(skill)
            for skill in new_candidate.soft_skills
        ]

        new_candidate_dict = {
            "user_id": new_candidate.user_id,
            "fullname": new_candidate.fullname,
            "soft_skills": soft_skill_objects,
            "tech_skills": tech_skill_objects,
        }

        await self.candidate_repository.create_candidate(new_candidate_dict)

    async def get_candidates_paginated(
        self, page: int, limit: int, tech_skills=None, soft_skills=None, id_list=None
    ):
        tech_skills_ids = [
            TechSkill.get_id_by_name(tech_skill) for tech_skill in tech_skills
        ]
        soft_skills_ids = [
            SoftSkill.get_id_by_name(soft_skill) for soft_skill in soft_skills
        ]

        return await self.candidate_repository.get_candidates_filtered(
            tech_skills_ids=tech_skills_ids,
            soft_skills_ids=soft_skills_ids,
            page=page,
            per_page=limit,
            ids=id_list,
        )
