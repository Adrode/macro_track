import pytest

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