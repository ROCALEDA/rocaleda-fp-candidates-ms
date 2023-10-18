from fastapi import FastAPI
from initializer import Initializer


app = FastAPI()

instances = Initializer(app)
instances.setup()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
