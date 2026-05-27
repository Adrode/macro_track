import pytest
from uuid import uuid4
import authentication.short_tokens as auth
from models.models import User

@pytest.fixture()
def test_user(db_session):
  user = User(
    email=f"adrian={uuid4()}@gmail.com",
    username="Adrian",
    hashed_password="fakehash",
    kcal_daily_goal=2000,
    protein_daily_goal=100,
    fat_daily_goal=70,
    carbs_daily_goal=250
  )
  db_session.add(user)
  db_session.commit()
  db_session.refresh(user)
  return user

def test_get_me_unauthorized(client):
  response = client.get("/users/")

  assert response.status_code == 401

def test_get_me_authorized(client, test_user):
  token = auth.create_access_token({
      "sub": test_user.email
    })
  response = client.get(
    "/users/",
    headers={"Authorization": f"Bearer {token}"}
  )

  data = response.json()

  assert response.status_code == 200
  assert "email" in data
  assert "id" in data
  
def test_patch_me_unauthorized(client, test_user):
  response = client.patch(
    "/users/",
    json={"username": test_user.username}
  )

  assert response.status_code == 401

def test_patch_me_authorized(client, test_user):
  token = auth.create_access_token({
      "sub": test_user.email
    })
  response = client.patch(
    "/users/",
    json={"username": "Adrian"},
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response.status_code == 200
  
  response2 = client.get(
    "/users/",
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response2.json()["username"] == "Adrian"

def test_patch_me_invalid_email(client, test_user):
  token = auth.create_access_token({
      "sub": test_user.email
    })
  response = client.patch(
    "/users/",
    json={"email": "kekw2"},
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response.status_code == 422