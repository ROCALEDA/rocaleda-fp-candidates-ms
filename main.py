from fastapi import FastAPI
from initializer import Initializer
from app.candidate.handlers.candidate_handlers import create_candidate_handler


app = FastAPI()

instances = Initializer(app)
instances.setup()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
