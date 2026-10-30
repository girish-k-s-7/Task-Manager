
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.task import Base, Task


# Create a separate in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite://"


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all registered tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Remove tables after the test session finishes
    Base.metadata.drop_all(bind=engine)

    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autocommit=False,
        autoflush=False,
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
