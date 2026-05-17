from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.db import engine, Base
from routes.task_route import route as task_route
from routes.auth_route import route as auth_route
import uvicorn
import models
from dotenv import load_dotenv


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(task_route)
app.include_router(auth_route)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
