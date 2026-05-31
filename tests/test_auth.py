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
  response1 = client.post(
    "/auth/register",
    json={
      "email": "adison@gmail.com",
      "username": "Nosida",
      "password": "hashfake",
      "kcal_daily_goal": 1500,
      "protein_daily_goal": 100,
      "fat_daily_goal": 70,
      "carbs_daily_goal": 150
    }
  )

  response2 = client.post(
    "/auth/register",
    json={
      "email": "adison@gmail.com",
      "username": "Nosida",
      "password": "hashfake",
      "kcal_daily_goal": 1500,
      "protein_daily_goal": 100,
      "fat_daily_goal": 70,
      "carbs_daily_goal": 150
    }
  )

  assert response1.status_code == 200
  assert response2.status_code == 400

def test_login_valid_data(client, test_first_user):
  response = client.post(
    "/auth/login",
    data={
      "username": test_first_user.email,
      "password": test_first_user.plain_password
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

def test_login_invalid_password(client, test_first_user):
  response = client.post(
    "/auth/login",
    data={
      "username": test_first_user.email,
      "password": "kekw"
    }
  )

  assert response.status_code == 401