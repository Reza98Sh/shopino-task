from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.router import router
from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Database initialized")
    yield
    print("Shutting down")


app = FastAPI(
    title="URL Shortener API",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
