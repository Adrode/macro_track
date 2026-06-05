def test_add_meal_valid_data(client, authenticate_first_user, test_first_product, test_public_product):
  response = client.post(
    "/meals/",
    json={
      "category": "dinner",
      "name": "Ziemniaczki and schabowi",
      "meal_products": [
        {
          "product_id": test_first_product.id,
          "grams": 100
        },
        {
          "product_id": test_public_product.id,
          "grams": 200
        }
      ]
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert response.json()["category"] == "dinner"

def test_add_meal_invalid_data(client, authenticate_first_user, test_public_product):
  response = client.post(
    "/meals/",
    json={
      "category": "something",
      "name": 15,
      "meal_products": [
        {
          "product_id": 10,
          "grams": "kekw"
        },
        {
          "product_id": test_public_product.id,
          "grams": 200
        }
      ]
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_add_meal_unauthorized(client, test_first_product):
  response = client.post(
    "/meals/",
    json={
      "category": "dinner",
      "name": "Ziemniaczki and schabowi",
      "meal_products": [
        {
          "product_id": test_first_product.id,
          "grams": 100
        },
        {
          "product_id": test_first_product.id,
          "grams": 200
        }
      ]
    }
  )

  assert response.status_code == 401

def test_add_meal_product_unauthorized(client, authenticate_first_user, test_second_product):
  response = client.post(
    "/meals/",
    json={
      "category": "dinner",
      "name": "Ziemniaczki and schabowi",
      "meal_products": [
        {
          "product_id": test_second_product.id,
          "grams": 100
        }
      ]
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_add_meal_invalid_product_id(client, authenticate_first_user):
  response = client.post(
    "/meals/",
    json={
      "category": "breakfast",
      "name": "Some shit",
      "meal_products": [
        {
          "product_id": 0,
          "grams": 100
        }
      ]
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_add_meal_invalid_product_grams(client, authenticate_first_user, test_first_product):
  response = client.post(
    "/meals/",
    json={
      "category": "breakfast",
      "name": "Some shit",
      "meal_products": [
        {
          "product_id": test_first_product.id,
          "grams": -100
        }
      ]
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_delete_meal_valid_data(client, authenticate_first_user, test_meal_first_user_1):
  response = client.delete(
    f"/meals/{test_meal_first_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert str(test_meal_first_user_1.id) in response.json()["detail"]

def test_delete_meal_unauthorized(client, test_meal_first_user_1):
  response = client.delete(
    f"/meals/{test_meal_first_user_1.id}"
  )

  assert response.status_code == 401

def test_delete_meal_not_found(client, authenticate_first_user):
  response = client.delete(
    "/meals/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_delete_meal_owned_by_other_user(client, authenticate_first_user, test_meal_second_user_1):
  response = client.delete(
    f"/meals/{test_meal_second_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_patch_is_active_valid_data(client, authenticate_first_user, test_meal_first_user_1):
  response = client.patch(
    f"/meals/is_active/{test_meal_first_user_1.id}",
    json={
      "is_active": False
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_patch_is_active_invalid_data(client, authenticate_first_user, test_meal_first_user_1):
  response = client.patch(
    f"/meals/is_active/{test_meal_first_user_1.id}",
    json={
      "is_active": "kekw"
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_patch_is_active_unauthorized(client, test_meal_first_user_1):
  response = client.patch(
    f"/meals/is_active/{test_meal_first_user_1.id}",
    json={
      "is_acitve": False
    }
  )

  assert response.status_code == 401

def test_patch_is_active_meal_not_found(client, authenticate_first_user):
  response = client.patch(
    "/meals/is_active/0",
    json={
      "is_active": False
      },
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_patch_is_active_meal_owned_by_other_user(client, authenticate_first_user, test_meal_second_user_1):
  response = client.patch(
    f"/meals/is_active/{test_meal_second_user_1.id}",
    json={
      "is_active": False
      },
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_patch_meal_valid_data(client, authenticate_first_user, test_meal_first_user_1, test_public_product):
  response = client.patch(
    f"/meals/{test_meal_first_user_1.id}",
    json={
      "category": "dinner",
      "name": "Podżabanyj",
      "meal_products": [
        {
          "product_id": test_public_product.id,
          "grams": 120
        }
      ]
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert "dinner" in response.json()["category"]
  assert "Podżabanyj" in response.json()["name"]

def test_patch_meal_invalid_data(client, authenticate_first_user, test_meal_first_user_1):
  response = client.patch(
    f"/meals/{test_meal_first_user_1.id}",
    json={
      "category": "nyb",
      "name": 120,
      "meal_products": [
        {
          "product_id": 350,
          "grams": -20
        }
      ]
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_patch_meal_unauthorized(client, test_meal_first_user_1, test_first_product):
  response = client.patch(
    f"/meals/{test_meal_first_user_1.id}",
    json={
      "category": "dinner",
      "name": "Podżabanyj",
      "meal_products": [
        {
          "product_id": test_first_product.id,
          "grams": 120
        }
      ]
    }
  )

  assert response.status_code == 401

def test_patch_meal_owned_by_other_user(client, authenticate_first_user, test_meal_second_user_1):
  response = client.patch(
    f"/meals/{test_meal_second_user_1.id}",
    json={
      "name": "kekw"
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_patch_meal_not_found(client, authenticate_first_user):
  response = client.patch(
    "/meals/0",
    json={
      "name": "Kekw"
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_patch_meal_unathorized_product(client, authenticate_first_user, test_meal_first_user_1, test_second_product):
  response = client.patch(
    f"/meals/{test_meal_first_user_1.id}",
    json={
      "meal_products": [
        {
          "product_id": test_second_product.id,
          "grams": 230
        }
      ]
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_get_meal_valid_data(client, authenticate_first_user, test_meal_first_user_1):
  response = client.get(
    f"/meals/{test_meal_first_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert test_meal_first_user_1.name in response.json()["name"]
  assert "category" in response.json()

def test_get_meal_unathorized(client, test_meal_first_user_1):
  response = client.get(
    f"/meals/{test_meal_first_user_1.id}"
  )

  assert response.status_code == 401

def test_get_meal_not_found(client, authenticate_first_user):
  response = client.get(
    "/meals/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_get_meal_owned_by_other_user(client, authenticate_first_user, test_meal_second_user_1):
  response = client.get(
    f"/meals/{test_meal_second_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 401

def test_get_is_active_meals_valid_data(client, authenticate_first_user, test_meal_first_user_1):
  response = client.get(
    "/meals/",
    headers=authenticate_first_user
  )
  
  assert response.status_code == 200
  for item in response.json():
    assert item["is_active"] == True

def test_get_is_active_meals_unathorized(client, test_meal_first_user_1):
  response = client.get(
    "/meals/"
  )

  assert response.status_code == 401

def test_get_is_active_meals_not_found(client, authenticate_first_user):
  response = client.get(
    "/meals/",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

# ---
def test_get_archived_meals_valid_data(client, authenticate_second_user, test_meal_second_user_2):
  response = client.get(
    "/meals/archived/",
    headers=authenticate_second_user
  )
  
  assert response.status_code == 200
  for item in response.json():
    assert item["is_active"] == False

def test_get_archived_meals_unathorized(client, test_meal_second_user_2):
  response = client.get(
    "/meals/archived/",
  )

  assert response.status_code == 401

def test_get_archived_meals_not_found(client, authenticate_first_user):
  response = client.get(
    "/meals/archived/",
    headers=authenticate_first_user
  )

  assert response.status_code == 404