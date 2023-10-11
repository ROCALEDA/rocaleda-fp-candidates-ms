from app.database.schemas import CreateCandidate
from app.candidate.repositories.candidate_repository import CandidateRepository


class CandidateService:
    def __init__(self, candidate_repository: CandidateRepository):
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
