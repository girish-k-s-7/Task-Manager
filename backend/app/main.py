from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.connection import engine
from app.models.task import Base, Task


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="Task Manager",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home_page():
    return {
        "App": "Task Manager",
        "Version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AI-Enhanced Task Manager"
    }
