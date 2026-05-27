import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool 
from sqlalchemy.orm import sessionmaker
from main import app
from database.database import get_db
from models.models import Base

engine = create_engine(
  "sqlite:///:memory:",
    # używa SQLite i trzyma bazę tylko w RAM, przez co jest szybko i baza znika po zakończeniu testów
  connect_args={"check_same_thread": False},
    # SQLite domyślnie robi jedno połączenie = jeden wątek, a TestClient/FastAPI mogą używać różnych threads, więc to pozwala na jedno połączenie
  poolclass=StaticPool
    # normalnie każde połączenie = nowa pusta baza, a ten zapis trzyma jedno połączenie "przy życiu"
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
  session = TestingSessionLocal()
  try:
    yield session
  finally:
    session.close()

app.dependency_overrides[get_db] = override_get_db
  # to powoduje przy testach użycie dla endpointów testowej DB, a nie produkcyjnej

@pytest.fixture(scope="session", autouse=True) # fixture to dane przygotowane pod testy
def setup_db():
    Base.metadata.create_all(bind=engine) # przed testami tworzy bazę
    yield
    Base.metadata.drop_all(bind=engine) # po testach zamyka bazę
  # scope="session" uruchamia ten setup dla całego pytest run, czyli:
  #   pytest start
  #   create tables
  #   wszystkie uruchomione testy
  #   pytest end
  #   drop tables
  # autouse=True czyli automatycznie używa setup dla każdego testu, więc nie trzeba tego pisać w arugmencie każdego testu

@pytest.fixture()
def client():
    return TestClient(app)
  # TestClient to po prostu fake client HTTP, czyli:
  #   nie odpala uvicorna
  #   nie otwiera portu
  #   nie ma prawdziwego networkingu
  # ale FastAPI zachowuje się tak samo jak przy prawdziwym request