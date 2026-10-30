
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL (configurable through environment variable)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./task_manager.db",
)

# Create SQLAlchemy database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
