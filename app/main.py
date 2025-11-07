from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.router import router
from app.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create all tables
    Base.metadata.create_all(bind=engine)
    print("Database initialized")
    yield
    print("Shutting down")

app = FastAPI(
    title="URL Shortener API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router, prefix="/api")
