import pytest
from uuid import uuid4
from models.models import User, Product
from authentication.pwd_hash import hash_password
from authentication.short_tokens import create_access_token

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


def test_post_product_valid_data(client, authenticate_first_user):
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
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert response.json()["category"] == "protein"
  assert "name" in response.json()
  assert response.json()["kcal_per_100g"] >= 0
  assert response.json()["protein_per_100g"] >= 0
  assert response.json()["fat_per_100g"] >= 0
  assert response.json()["carbs_per_100g"] >= 0
                
def test_post_product_invalid_data(client, authenticate_first_user):
  response = client.post(
    "/products/",
    json={
      "category": "breakfast",
      "name": 15,
      "kcal_per_100g": "kekw",
      "protein_per_100g": -20,
      "fat_per_100g": 0,
      "carbs_per_100g": 45
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_get_product_valid_data(client, test_first_product, authenticate_first_user):
  response = client.get(
    f"/products/{test_first_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_get_product_unauthorized_user(client, test_first_product):
  response = client.get(
    f"/products/{test_first_product.id}"
  )

  assert response.status_code == 401

def test_get_product_owned_by_other_user(client, test_second_product, authenticate_first_user):
  response = client.get(
    f"/products/{test_second_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_get_product_does_not_exist(client, authenticate_first_user):
  response = client.get(
    "/products/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_get_products_valid_data(
    client,
    authenticate_first_user,
    authenticate_second_user,
    test_public_product,
    test_first_product,
    test_second_product
  ):
  response1 = client.get(
    "/products/",
    headers=authenticate_first_user
  )
  
  response2 = client.get(
    "/products/",
    headers=authenticate_second_user
  )
  
  assert response1.status_code == 200
  assert response2.status_code == 200

def test_get_products_unauthorized(client, test_first_product, test_public_product):
  response = client.get(
    "/products/"
  )

  assert response.status_code == 401

def test_get_products_no_products_in_db(client, authenticate_first_user, authenticate_second_user):
  response1 = client.get(
    "/products/",
    headers=authenticate_first_user
  )

  response2 = client.get(
    "/products/",
    headers=authenticate_second_user
  )

  assert response1.status_code == 404
  assert response2.status_code == 404

def test_get_products_only_public(client, authenticate_first_user, authenticate_second_user, test_public_product):
  response1 = client.get(
    "/products/",
    headers=authenticate_first_user
  )

  response2 = client.get(
    "/products/",
    headers=authenticate_second_user
  )

  assert response1.status_code == 200
  assert response2.status_code == 200
  assert response1.json() == response2.json()

def test_delete_product_valid_data(client, authenticate_first_user, test_first_product):
  response = client.delete(
    f"/products/{test_first_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_delete_product_unauthorized(client, test_first_product):
  response = client.delete(
    f"/products/{test_first_product.id}"
  )

  assert response.status_code == 401

def test_delete_product_owned_by_other_user(client, test_second_product, authenticate_first_user):
  response = client.delete(
    f"/products/{test_second_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_delete_product_public(client, authenticate_first_user, test_public_product):
  response = client.delete(
    f"/products/{test_public_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_delete_product_does_not_exist(client, authenticate_first_user):
  response = client.delete(
    f"/products/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 404