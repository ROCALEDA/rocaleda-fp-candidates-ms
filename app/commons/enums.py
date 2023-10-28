from enum import Enum


class SoftSkill(Enum):
    Leadership = 1
    Responsibility = 2
    Ownership = 3
    Communication = 4
    Teamwork = 5
    Adaptability = 6
    Empathy = 7
    Management = 8

    @classmethod
    def get_id_by_name(cls, name):
        for skill in cls:
            if skill.name == name:
                return skill.value
        raise ValueError(f"Soft skill '{name}' not found")


class TechSkill(Enum):
    Frontend = 1
    Backend = 2
    ReactJS = 3
    NodeJS = 4
    NextJS = 5
    Python = 6
    Flask = 7
    AWS = 8
    Architecture = 9
    NestJS = 10
    Angular = 11
    GCP = 12
    Azure = 13
    DevOps = 14
    Java = 15
    SpringBoot = 16
    FastAPI = 17
    Data_Science = 18
    SQL = 19
    NoSQL = 20
    MongoDB = 21
    Redis = 22
    CSS = 23
    TypeScript = 24

    @classmethod
    def get_id_by_name(cls, name):
        for skill in cls:
            if skill.name.replace("_", " ") == name:
                return skill.value
        raise ValueError(f"Tech skill '{name}' not found")
