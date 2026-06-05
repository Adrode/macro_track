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

