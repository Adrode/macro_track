from datetime import datetime
from models.models import Meal, MealProduct, DiaryMealProduct

def test_post_diary_valid_data(client, authenticate_first_user, test_meal_first_user_1):
  response = client.post(
    "/user/diary/",
    json={
      "meal_id": test_meal_first_user_1.id,
      "meal_datetime": datetime(2026, 5, 10, 8, 30).isoformat()
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_post_diary_invalid_data(client, authenticate_first_user):
  response = client.post(
    "/user/diary/",
    json={
      "meal_id": 0,
      "meal_datetime": "kekw"
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_post_diary_unauthorized(client, test_meal_first_user_1):
  response = client.post(
    "/user/diary/",
    json={
      "meal_id": test_meal_first_user_1.id
    }
  )

  assert response.status_code == 401

def test_get_diary_valid_data(client, authenticate_second_user, test_diary_second_user_1):
  response = client.get(
    f"/user/diary/entry/{test_diary_second_user_1.id}",
    headers=authenticate_second_user
  )

  assert response.status_code == 200

def test_get_diary_returns_meal_products_payload(client, authenticate_first_user, test_meal_first_user_1):
  response = client.post(
    "/user/diary/",
    json={
      "meal_id": test_meal_first_user_1.id,
      "meal_datetime": datetime(2026, 5, 10, 8, 30).isoformat()
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  diary_id = response.json()["id"]

  response = client.get(
    f"/user/diary/entry/{diary_id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert response.json()["meal_name"] == test_meal_first_user_1.name
  assert len(response.json()["meal_products"]) == 2
  assert {item["product_name"] for item in response.json()["meal_products"]} == {"Pierogies", "Baton"}

def test_get_diary_unauthorized(client, test_diary_second_user_1):
  response = client.get(
    f"/user/diary/entry/{test_diary_second_user_1.id}"
  )

  assert response.status_code == 401

def test_get_diary_invalid_id(client, authenticate_second_user):
  response = client.get(
    "/user/diary/entry/0",
    headers=authenticate_second_user
  )

  assert response.status_code == 404

def test_get_diary_owned_by_other_user(client, authenticate_second_user, test_diary_first_user_1):
  response = client.get(
    f"/user/diary/entry/{test_diary_first_user_1.id}",
    headers=authenticate_second_user
  )

  assert response.status_code == 404

def test_get_diaries_by_date_valid_data(client, authenticate_second_user, test_diary_second_user_1, test_diary_second_user_2):
  response = client.get(
    f"/user/diary/{datetime(2026, 5, 10)}",
    headers=authenticate_second_user
  )

  assert response.status_code == 200

def test_get_diaries_by_date_invalid_data(client, authenticate_second_user, test_diary_second_user_1, test_diary_second_user_2):
  response = client.get(
    "/user/diary/0",
    headers=authenticate_second_user
  )

  assert response.status_code == 404

def test_get_diaries_by_date_unauthorized(client, test_diary_second_user_1, test_diary_second_user_2):
  response = client.get(
    f"/user/diary/{datetime(2026, 5, 10)}"
  )

  assert response.status_code == 401

def test_get_diaries_by_date_not_found(client, authenticate_second_user):
  response = client.get(
    f"/user/diary/{datetime(2026, 5, 10)}",
    headers=authenticate_second_user
  )

  assert response.status_code == 404

def test_get_diaries_by_date_owned_by_other_user(client, authenticate_second_user, test_diary_first_user_1):
  response = client.get(
    f"/user/diary/{datetime(2026, 5, 6)}",
    headers=authenticate_second_user
  )

  assert response.status_code == 404

def test_get_diaries_valid_data(client, authenticate_second_user, test_diary_second_user_1, test_diary_second_user_2):
  response = client.get(
    "/user/diary/",
    headers=authenticate_second_user
  )

  assert response.status_code == 200

def test_get_diaries_unauthorized(client, test_diary_second_user_1, test_diary_second_user_2):
  response = client.get(
    "/user/diary/"
  )

  assert response.status_code == 401

def test_get_diaries_not_found(client, authenticate_first_user):
  response = client.get(
    "/user/diary/",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_delete_diary_valid_data(client, authenticate_first_user, test_diary_first_user_1):
  response = client.delete(
    f"/user/diary/{test_diary_first_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_delete_diary_removes_related_products(
  client,
  authenticate_first_user,
  db_session,
  test_meal_first_user_1,
  test_first_user
):
  response = client.post(
    "/user/diary/",
    json={
      "meal_id": test_meal_first_user_1.id,
      "meal_datetime": datetime(2026, 5, 10, 8, 30).isoformat()
    },
    headers=authenticate_first_user
  )

  diary_id = response.json()["id"]

  assert response.status_code == 200
  assert db_session.query(DiaryMealProduct).filter_by(diary_id=diary_id).count() == 2

  response = client.delete(
    f"/user/diary/{diary_id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert db_session.query(DiaryMealProduct).filter_by(diary_id=diary_id).count() == 0

def test_delete_diary_unathorized(client, test_diary_first_user_1):
  response = client.delete(
    f"/user/diary/{test_diary_first_user_1.id}"
  )

  assert response.status_code == 401

def test_delete_diary_owned_by_other_user(client, authenticate_first_user, test_diary_second_user_1):
  response = client.delete(
    f"/user/diary/{test_diary_second_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_delete_diary_not_found(client, authenticate_first_user):
  response = client.delete(
    "/user/diary/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_patch_diary_valid_data(client, authenticate_first_user, test_diary_first_user_1):
  response = client.patch(
    f"/user/diary/{test_diary_first_user_1.id}",
    json={
      "meal_datetime": datetime.now().isoformat()
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_patch_diary_replaces_meal_and_products(
  client,
  authenticate_first_user,
  db_session,
  test_first_user,
  test_public_product,
  test_diary_first_user_1
):
  new_meal = Meal(
    category="lunch",
    name="Risotto",
    user_id=test_first_user.id,
    source="user"
  )

  db_session.add(new_meal)
  db_session.flush()

  db_session.add(MealProduct(
    meal_id=new_meal.id,
    product_id=test_public_product.id,
    grams=250
  ))
  db_session.commit()
  db_session.refresh(new_meal)

  response = client.patch(
    f"/user/diary/{test_diary_first_user_1.id}",
    json={
      "meal_id": new_meal.id
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert response.json()["meal_name"] == "Risotto"
  assert db_session.query(DiaryMealProduct).filter_by(diary_id=test_diary_first_user_1.id).count() == 1


def test_patch_diary_invalid_data(client, authenticate_first_user, test_diary_first_user_1):
  response = client.patch(
    f"/user/diary/{test_diary_first_user_1.id}",
    json={
      "meal_id": "kekw",
      "meal_datetime": "bim bam"
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_patch_diary_unauthorized(client, test_diary_first_user_1):
  response = client.patch(
    f"/user/diary/{test_diary_first_user_1.id}",
    json={
      "meal_datetime": datetime.now().isoformat()
    }
  )

  assert response.status_code == 401

def test_patch_diary_owned_by_other_user(client, authenticate_first_user, test_diary_second_user_1):
  response = client.patch(
    f"/user/diary/{test_diary_second_user_1.id}",
    json={
      "meal_datetime": datetime.now().isoformat()
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_patch_diary_not_found(client, authenticate_first_user):
  response = client.patch(
    "/user/diary/0",
    json={
      "meal_datetime": datetime.now().isoformat()
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_patch_diary_unathorized_meal(client, authenticate_first_user, test_diary_first_user_1, test_meal_second_user_1):
  response = client.patch(
    f"/user/diary/{test_diary_first_user_1.id}",
    json={
      "meal_id": test_meal_second_user_1.id
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 404