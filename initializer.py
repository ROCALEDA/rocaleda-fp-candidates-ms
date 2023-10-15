from fastapi import FastAPI

from app.database import models, database
from app.health.controllers import health_controller
from app.health.services.health_service import HealthService
from app.candidate.services.candidate_service import CandidateService
from app.candidate.repositories.candidate_repository import CandidateRepository

class Initializer:
    def __init__(self, app: FastAPI):
        self.app = app
        self.candidate_service = None

    def setup(self):
        self.init_health_module()
        self.init_candidate_module()
        self.init_database()

    def init_health_module(self):
        health_service = HealthService()
        health_controller.initialize(health_service)
        self.app.include_router(health_controller.router)

    def init_candidate_module(self):
        candidate_repository = CandidateRepository()
        candidate_service = CandidateService(candidate_repository)
        self.candidate_service = candidate_service
        
    def init_database(self):
        models.Base.metadata.create_all(bind=database.engine)
