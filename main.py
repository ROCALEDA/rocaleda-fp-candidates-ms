import asyncio
from dotenv import load_dotenv


load_dotenv()

from app.commons.gcp import (
    pull_messages,
    create_candidate_sub,
    CANDIDATE_CREATION_SUB_PATH,
)
from fastapi import FastAPI
from initializer import Initializer
from app.candidate.handlers.candidate_handlers import create_candidate_handler


app = FastAPI()

instances = Initializer(app)
instances.setup()


@app.on_event("startup")
async def on_startup() -> None:
    asyncio.create_task(
        pull_messages(
            create_candidate_sub,
            CANDIDATE_CREATION_SUB_PATH,
            create_candidate_handler(instances.candidate_service),
        )
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
