import pytest
from app.main import app
from fastapi.testclient import TestClient
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dependencies import get_db
from app.database import Base

test_engine = create_engine(settings.TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(
    bind= test_engine,
    autoflush= False,
    autocommit= False
)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def client():
    return TestClient(app)
