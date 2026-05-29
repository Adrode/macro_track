import pytest, json
from uuid import uuid4
from models.models import User
from authentication.pwd_hash import hash_password

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

def test_register_valid_data(client):
  response = client.post(
    "/auth/register",
    json={
      "email": f"adison@gmail.com",
      "username": "Adison",
      "password": "fakehash",
      "kcal_daily_goal": 3000,
      "protein_daily_goal": 150,
      "fat_daily_goal": 70,
      "carbs_daily_goal": 300
    }
  )

  assert response.status_code == 200
  assert response.json()["email"] == "adison@gmail.com"
  assert "id" in response.json()

def test_register_invalid_email(client):
  response = client.post(
    "/auth/register",
    json={
      "email": f"gmail.com",
      "username": "g",
      "password": "fakehash",
      "kcal_daily_goal": 3000,
      "protein_daily_goal": 150,
      "fat_daily_goal": 70,
      "carbs_daily_goal": 300
    }
  )

  assert response.status_code == 422

def test_register_duplicated_email(client):
  response = client.post(
    "/auth/register",
    json={
      "email": f"adison@gmail.com",
      "username": "Nosida",
      "password": "hashfake",
      "kcal_daily_goal": 1500,
      "protein_daily_goal": 100,
      "fat_daily_goal": 70,
      "carbs_daily_goal": 150
    }
  )

  assert response.status_code == 400

def test_login_valid_data(client, test_user):
  response = client.post(
    "/auth/login",
    data={
      "username": test_user.email,
      "password": test_user.plain_password
    }
  )

  assert response.status_code == 200
  assert "access_token" in response.json()

def test_login_invalid_data(client):
  response = client.post(
    "/auth/login",
    data={
      "username": "kekw",
      "password": "kekw"
    }
  )

  assert response.status_code == 401

def test_login_invalid_password(client, test_user):
  response = client.post(
    "/auth/login",
    data={
      "username": test_user.email,
      "password": "kekw"
    }
  )

  assert response.status_code == 401