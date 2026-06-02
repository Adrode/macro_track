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

def test_delete_meal_does_not_exist(client, authenticate_first_user):
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