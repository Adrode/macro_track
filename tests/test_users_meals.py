def test_add_meal_valid_data(client, authenticate_first_user, test_first_product, test_public_product):
  response = client.post(
    "/user/meals/",
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
    "/user/meals/",
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

def test_add_meal_without_meal_products(client, authenticate_first_user, test_public_product):
  response = client.post(
    "/user/meals/",
    json={
      "category": "dinner",
      "name": "Pierogies",
      "meal_products": []
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_add_meal_unauthorized(client, test_first_product):
  response = client.post(
    "/user/meals/",
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
    "/user/meals/",
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

  assert response.status_code == 404

def test_add_meal_invalid_product_id(client, authenticate_first_user):
  response = client.post(
    "/user/meals/",
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

  assert response.status_code == 404

def test_add_meal_invalid_product_grams(client, authenticate_first_user, test_first_product):
  response = client.post(
    "/user/meals/",
    json={
      "category": "breakfast",
      "name": "Someshing",
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
    f"/user/meals/{test_meal_first_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert str(test_meal_first_user_1.id) in response.json()["detail"]

def test_delete_meal_unauthorized(client, test_meal_first_user_1):
  response = client.delete(
    f"/user/meals/{test_meal_first_user_1.id}"
  )

  assert response.status_code == 401

def test_delete_meal_not_found(client, authenticate_first_user):
  response = client.delete(
    "/user/meals/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_delete_meal_owned_by_other_user(client, authenticate_first_user, test_meal_second_user_1):
  response = client.delete(
    f"/user/meals/{test_meal_second_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_patch_meal_valid_data(client, authenticate_first_user, test_meal_first_user_1, test_public_product):
  response = client.patch(
    f"/user/meals/{test_meal_first_user_1.id}",
    json={
      "category": "dinner",
      "name": "Abrakadabra",
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
  assert "Abrakadabra" in response.json()["name"]

def test_patch_meal_no_changes(client, authenticate_first_user, test_meal_first_user_1):
  response = client.patch(
    f"/user/meals/{test_meal_first_user_1.id}",
    json={},
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_patch_meal_one_change(client, authenticate_first_user, test_meal_first_user_1, test_public_product):
  response = client.patch(
    f"/user/meals/{test_meal_first_user_1.id}",
    json={
      "name": "Capybara"
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert "Capybara" in response.json()["name"]

def test_patch_meal_invalid_data(client, authenticate_first_user, test_meal_first_user_1):
  response = client.patch(
    f"/user/meals/{test_meal_first_user_1.id}",
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
    f"/user/meals/{test_meal_first_user_1.id}",
    json={
      "category": "dinner",
      "name": "Cytryna",
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
    f"/user/meals/{test_meal_second_user_1.id}",
    json={
      "name": "kekw"
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_patch_meal_not_found(client, authenticate_first_user):
  response = client.patch(
    "/user/meals/0",
    json={
      "name": "Kekw"
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_patch_meal_unathorized_product(client, authenticate_first_user, test_meal_first_user_1, test_second_product):
  response = client.patch(
    f"/user/meals/{test_meal_first_user_1.id}",
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

  assert response.status_code == 404
  assert response.json()["detail"] == "Product not found"

def test_get_meal_valid_data(client, authenticate_first_user, test_meal_first_user_1):
  response = client.get(
    f"/user/meals/{test_meal_first_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert test_meal_first_user_1.name in response.json()["name"]
  assert "category" in response.json()

def test_get_meal_unathorized(client, test_meal_first_user_1):
  response = client.get(
    f"/user/meals/{test_meal_first_user_1.id}"
  )

  assert response.status_code == 401

def test_get_meal_not_found(client, authenticate_first_user):
  response = client.get(
    "/user/meals/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_get_meal_owned_by_other_user(client, authenticate_first_user, test_meal_second_user_1):
  response = client.get(
    f"/user/meals/{test_meal_second_user_1.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_get_meals_valid_data(client, authenticate_second_user, test_meal_second_user_1, test_meal_second_user_2):
  response = client.get(
    "/user/meals/",
    headers=authenticate_second_user
  )

  assert response.status_code == 200

def test_get_meals_not_found(client, authenticate_second_user):
  response = client.get(
    "/user/meals/",
    headers=authenticate_second_user
  )

  assert response.status_code == 404