from datetime import datetime

def test_post_diary_valid_data(client, authenticate_first_user, test_meal_first_user_1):
  response = client.post(
    "/diary/",
    json={
      "meal_id": test_meal_first_user_1.id
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_post_diary_invalid_data(client, authenticate_first_user):
  response = client.post(
    "/diary/",
    json={
      "meal_id": 0,
      "meal_datetime": "kekw"
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_post_diary_unauthorized(client, test_meal_first_user_1):
  response = client.post(
    "/diary/",
    json={
      "meal_id": test_meal_first_user_1.id
    }
  )

  assert response.status_code == 401

def test_post_diary_inactive_meal(client, authenticate_second_user, test_meal_second_user_2):
  response = client.post(
    "/diary/",
    json={
      "meal_id": test_meal_second_user_2.id
    },
    headers=authenticate_second_user
  )

  assert response.status_code == 400

def test_get_diary_by_id_valid_data(client, authenticate_second_user, test_diary_second_user_1):
  response = client.get(
    f"/diary/entry/{test_diary_second_user_1.id}",
    headers=authenticate_second_user
  )

  assert response.status_code == 200

def test_get_diary_by_id_unauthorized(client, test_diary_second_user_1):
  response = client.get(
    f"/diary/entry/{test_diary_second_user_1.id}"
  )

  assert response.status_code == 401

def test_get_diary_by_id_invalid_id(client, authenticate_second_user):
  response = client.get(
    "/diary/entry/0",
    headers=authenticate_second_user
  )

  assert response.status_code == 401

def test_get_diary_by_id_owned_by_other_user(client, authenticate_second_user, test_diary_first_user_1):
  response = client.get(
    f"/diary/entry/{test_diary_first_user_1.id}",
    headers=authenticate_second_user
  )

  assert response.status_code == 401

def test_get_diaries_by_date_valid_data(client, authenticate_second_user, test_diary_second_user_1, test_diary_second_user_2):
  response = client.get(
    f"/diary/{datetime(2026, 5, 10)}",
    headers=authenticate_second_user
  )

  assert response.status_code == 200

def test_get_diaries_by_date_invalid_data(client, authenticate_second_user, test_diary_second_user_1, test_diary_second_user_2):
  response = client.get(
    "/diary/0",
    headers=authenticate_second_user
  )

  assert response.status_code == 401

def test_get_diaries_by_date_unauthorized(client, test_diary_second_user_1, test_diary_second_user_2):
  response = client.get(
    f"/diary/{datetime(2026, 5, 10)}"
  )

  assert response.status_code == 401

def test_get_diaries_by_date_not_found(client, authenticate_second_user):
  response = client.get(
    f"/diary/{datetime(2026, 5, 10)}",
    headers=authenticate_second_user
  )

  assert response.status_code == 401

def test_get_diaries_by_date_owned_by_other_user(client, authenticate_second_user, test_diary_first_user_1):
  response = client.get(
    f"/diary/{datetime(2026, 5, 6)}",
    headers=authenticate_second_user
  )

  assert response.status_code == 401

def test_get_all_diaries_valid_data(client, authenticate_second_user, test_diary_second_user_1, test_diary_second_user_2):
  response = client.get(
    "/diary/",
    headers=authenticate_second_user
  )

  assert response.status_code == 200

def test_get_all_diaries_unauthorized(client, test_diary_second_user_1, test_diary_second_user_2):
  response = client.get(
    "/diary/"
  )

  assert response.status_code == 401

def test_get_all_diaries_not_found(client, authenticate_first_user):
  response = client.get(
    "/diary/",
    headers=authenticate_first_user
  )

  assert response.status_code == 401
  assert "Diaries not found" in response.json()["detail"]

def test_delete_diary_valid_data(client, authenticate_first_user, test_diary_first_user_1):
  response = client.delete(
    f"/diary/{test_diary_first_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_delete_diary_invalid_data(client, authenticate_first_user, test_diary_first_user_1):
  response = client.delete(
    "/diary/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_delete_diary_unathorized(client, test_diary_first_user_1):
  response = client.delete(
    f"/diary/{test_diary_first_user_1.id}"
  )

  assert response.status_code == 401

def test_delete_diary_owned_by_other_user(client, authenticate_first_user, test_diary_second_user_1):
  response = client.delete(
    f"/diary/{test_diary_second_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_delete_diary_not_found(client, authenticate_first_user):
  response = client.delete(
    "/diary/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 401
  assert "Diaries not found" in response.json()["detail"]