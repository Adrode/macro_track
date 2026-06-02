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

def test_add_meal_invalid_products(client, authenticate_first_user):
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