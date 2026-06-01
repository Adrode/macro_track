import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool, delete
from sqlalchemy.orm import sessionmaker
from main import app
from database.database import get_db
from models.models import Base, Product, User, Meal, MealProduct
from authentication.pwd_hash import hash_password

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
def db_session():
  session = TestingSessionLocal()
  try:
    yield session
  finally:
    session.close()

@pytest.fixture()
def client():
  return TestClient(app)
  # TestClient to po prostu fake client HTTP, czyli:
  #   nie odpala uvicorna
  #   nie otwiera portu
  #   nie ma prawdziwego networkingu
  # ale FastAPI zachowuje się tak samo jak przy prawdziwym request

@pytest.fixture(autouse=True)
def clean_db(db_session):
  yield
  db_session.execute(delete(Product))
  db_session.execute(delete(User))
  db_session.commit()


@pytest.fixture()
def test_first_user(db_session):
  password = "fakehash"

  user = User(
    email=f"adrian-{uuid4()}@gmail.com",
    username="Adrian",
    hashed_password=hash_password(password),
    kcal_daily_goal=2000,
    protein_daily_goal=100,
    fat_daily_goal=70,
    carbs_daily_goal=250
  )

  db_session.add(user)
  db_session.commit()
  db_session.refresh(user)

  user.plain_password = password

  return user

@pytest.fixture()
def test_second_user(db_session):
  password = "hashfake"

  user = User(
    email=f"second-{uuid4()}@gmail.com",
    username="Second",
    hashed_password=hash_password(password),
    kcal_daily_goal=3000,
    protein_daily_goal=150,
    fat_daily_goal=70,
    carbs_daily_goal=300
  )

  db_session.add(user)
  db_session.commit()
  db_session.refresh(user)

  user.plain_password = password

  return user

@pytest.fixture()
def token_first_user(client, test_first_user):
  response = client.post(
    "/auth/login",
    data={
      "username": test_first_user.email,
      "password": test_first_user.plain_password
    }
  )

  token = response.json()["access_token"]

  return token

@pytest.fixture()
def token_second_user(client, test_second_user):
  response = client.post(
    "/auth/login",
    data={
      "username": test_second_user.email,
      "password": test_second_user.plain_password
    }
  )

  token = response.json()["access_token"]

  return token

@pytest.fixture()
def authenticate_first_user(token_first_user):
  return {"Authorization": f"Bearer {token_first_user}"}

@pytest.fixture()
def authenticate_second_user(token_second_user):
  return {"Authorization": f"Bearer {token_second_user}"}

@pytest.fixture()
def test_public_product(db_session):
  product = Product(
    category="carbs",
    name="Baton",
    kcal_per_100g=150,
    protein_per_100g=20,
    fat_per_100g=5,
    carbs_per_100g=45,
    user_id=None
  )

  db_session.add(product)
  db_session.commit()
  db_session.refresh(product)

  return product

@pytest.fixture()
def test_first_product(db_session, test_first_user):
  product = Product(
    category="carbs",
    name="Pierogies",
    kcal_per_100g=150,
    protein_per_100g=20,
    fat_per_100g=5,
    carbs_per_100g=45,
    user_id=test_first_user.id
  )

  db_session.add(product)
  db_session.commit()
  db_session.refresh(product)

  return product

@pytest.fixture()
def test_second_product(db_session, test_second_user):
  product = Product(
    category="carbs",
    name="Macaronis",
    kcal_per_100g=350,
    protein_per_100g=10,
    fat_per_100g=10,
    carbs_per_100g=60,
    user_id=test_second_user.id
  )

  db_session.add(product)
  db_session.commit()
  db_session.refresh(product)

  return product

# --- MEAL 1, FIRST USER
@pytest.fixture()
def test_meal_product_first_user_1(db_session, test_first_product):
  meal_product = MealProduct(
    product_id=test_first_product.id,
    grams=100
  )

  db_session.add(meal_product)
  db_session.commit()
  db_session.refresh(meal_product)

  return meal_product

@pytest.fixture()
def test_meal_product_first_user_2(db_session, test_public_product):
  meal_product = MealProduct(
    product_id=test_public_product.id,
    grams=200
  )

  db_session.add(meal_product)
  db_session.commit()
  db_session.refresh(meal_product)

  return meal_product

@pytest.fixture()
def test_meal_first_user_1(
  db_session,
  test_first_user,
  test_meal_product_first_user_1,
  test_meal_product_first_user_2
):
  meal = Meal(
    category="breakfast",
    name="Oatmeal",
    meal_products=[
      test_meal_product_first_user_1,
      test_meal_product_first_user_2
    ],
    user_id=test_first_user.id
  )

  db_session.add(meal)
  db_session.commit()
  db_session.refresh(meal)
# ---

# --- MEAL 1, SECOND USER
@pytest.fixture()
def test_meal_product_second_user_1(db_session, test_second_product):
  meal_product = MealProduct(
    product_id=test_second_product.id,
    grams=150
  )

  db_session.add(meal_product)
  db_session.commit()
  db_session.refresh(meal_product)

  return meal_product

@pytest.fixture()
def test_meal_second_user_1(
  db_session,
  test_second_user,
  test_meal_product_second_user_1
):
  meal = Meal(
    category="breakfast",
    name="Oatmeal",
    meal_products=[
      test_meal_product_second_user_1
    ],
    user_id=test_second_user.id
  )

  db_session.add(meal)
  db_session.commit()
  db_session.refresh(meal)

  return meal
# ---

# --- MEAL 2, SECOND USER
@pytest.fixture()
def test_meal_product_second_user_2(db_session, test_public_product):
  meal_product = MealProduct(
    product_id=test_public_product.id,
    grams=250
  )

  db_session.add(meal_product)
  db_session.commit()
  db_session.refresh(meal_product)

  return meal_product

@pytest.fixture()
def test_meal_second_user_2(
  db_session,
  test_second_user,
  test_meal_product_second_user_2
):
  meal = Meal(
    category="breakfast",
    name="Oatmeal",
    meal_products=[
      test_meal_product_second_user_2
    ],
    user_id=test_second_user.id
  )

  db_session.add(meal)
  db_session.commit()
  db_session.refresh(meal)

  return meal
# ---