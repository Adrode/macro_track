import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool 
from sqlalchemy.orm import sessionmaker
from main import app
from database.database import get_db
from models.models import Base

engine = create_engine(
  "sqlite:///:memory:",
  connect_args={"check_same_thread": False},
  poolclass=StaticPool  
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
  session = TestingSessionLocal()
  try:
    yield session
  finally:
    session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    return TestClient(app)