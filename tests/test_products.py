import pytest
from uuid import uuid4
from models.models import User, Product
from authentication.pwd_hash import hash_password
from authentication.short_tokens import create_access_token

@pytest.fixture()
def test_user(db_session):
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
def token(client, test_user):
  response = client.post(
    "/auth/login",
    data={
      "username": test_user.email,
      "password": test_user.plain_password
    }
  )

  token = response.json()["access_token"]

  return token

@pytest.fixture()
def authenticate_user(token):
  return {"Authorization": f"Bearer {token}"}

@pytest.fixture()
def test_product(db_session, test_user):
  product = Product(
    category="carbs",
    name="Pierogies",
    kcal_per_100g=150,
    protein_per_100g=20,
    fat_per_100g=5,
    carbs_per_100g=45,
    user_id=test_user.id
  )

  db_session.add(product)
  db_session.commit()
  db_session.refresh(product)

  return product

def test_post_product_valid_data(client, authenticate_user):
  response = client.post(
    "/products/",
    json={
      "category": "protein",
      "name": "Parówkas",
      "kcal_per_100g": 150,
      "protein_per_100g": 20,
      "fat_per_100g": 5,
      "carbs_per_100g": 45
    },
    headers=authenticate_user
  )

  assert response.status_code == 200