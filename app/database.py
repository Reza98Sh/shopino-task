from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Create a synchronous Engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=settings.pool_pre_ping,
    pool_size=settings.pool_size,
    max_overflow=settings.max_overflow,
)

# Create SessionLocal factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all models
Base = declarative_base()


def get_db():
    """
    Dependency -- yields a SQLAlchemy Session, then closes it.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
