def test_post_product_valid_data(client, authenticate_first_user):
  response = client.post(
    "/user/products/",
    json={
      "category": "protein",
      "name": "Parówkas",
      "kcal_per_100g": 150,
      "protein_per_100g": 20,
      "fat_per_100g": 5,
      "carbs_per_100g": 45
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert response.json()["category"] == "protein"
  assert "name" in response.json()
  assert response.json()["kcal_per_100g"] >= 0
  assert response.json()["protein_per_100g"] >= 0
  assert response.json()["fat_per_100g"] >= 0
  assert response.json()["carbs_per_100g"] >= 0
                
def test_post_product_invalid_data(client, authenticate_first_user):
  response = client.post(
    "/user/products/",
    json={
      "category": "breakfast",
      "name": 15,
      "kcal_per_100g": "kekw",
      "protein_per_100g": -20,
      "fat_per_100g": 0,
      "carbs_per_100g": 45
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_post_product_macros_lower_than_zero(client, authenticate_first_user):
  response = client.post(
    "/user/products/",
    json={
      "category": "protein",
      "name": "whey",
      "kcal_per_100g": -200,
      "protein_per_100g": -20,
      "fat_per_100g": -10,
      "carbs_per_100g": -50
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_get_product_valid_data(client, test_first_product, authenticate_first_user):
  response = client.get(
    f"/user/products/{test_first_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_get_product_unauthorized_user(client, test_first_product):
  response = client.get(
    f"/user/products/{test_first_product.id}"
  )

  assert response.status_code == 401

def test_get_product_owned_by_other_user(client, test_second_product, authenticate_first_user):
  response = client.get(
    f"/user/products/{test_second_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_get_product_does_not_exist(client, authenticate_first_user):
  response = client.get(
    "/user/products/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_get_product_public(client, authenticate_first_user, test_public_product):
  response = client.get(
    f"/user/products/{test_public_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_get_products_valid_data(
    client,
    authenticate_first_user,
    authenticate_second_user,
    test_public_product,
    test_first_product,
    test_second_product
  ):
  response1 = client.get(
    "/user/products/",
    headers=authenticate_first_user
  )
  
  response2 = client.get(
    "/user/products/",
    headers=authenticate_second_user
  )
  
  assert response1.status_code == 200
  assert response2.status_code == 200

def test_get_products_unauthorized(client, test_first_product, test_public_product):
  response = client.get(
    "/user/products/"
  )

  assert response.status_code == 401

def test_get_products_no_products_in_db(client, authenticate_first_user, authenticate_second_user):
  response1 = client.get(
    "/user/products/",
    headers=authenticate_first_user
  )

  response2 = client.get(
    "/user/products/",
    headers=authenticate_second_user
  )

  assert response1.status_code == 404
  assert response2.status_code == 404

def test_get_products_only_public(client, authenticate_first_user, authenticate_second_user, test_public_product):
  response1 = client.get(
    "/user/products/",
    headers=authenticate_first_user
  )

  response2 = client.get(
    "/user/products/",
    headers=authenticate_second_user
  )

  assert response1.status_code == 200
  assert response2.status_code == 200
  assert response1.json() == response2.json()

def test_delete_product_valid_data(client, authenticate_first_user, test_first_product):
  response = client.delete(
    f"/user/products/{test_first_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_delete_product_unauthorized(client, test_first_product):
  response = client.delete(
    f"/user/products/{test_first_product.id}"
  )

  assert response.status_code == 401

def test_delete_product_owned_by_other_user(client, test_second_product, authenticate_first_user):
  response = client.delete(
    f"/user/products/{test_second_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_delete_product_public(client, authenticate_first_user, test_public_product):
  response = client.delete(
    f"/user/products/{test_public_product.id}",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_delete_product_does_not_exist(client, authenticate_first_user):
  response = client.delete(
    f"/user/products/0",
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_patch_product_valid_data(client, authenticate_first_user, test_first_product):
  response = client.patch(
    f"/user/products/{test_first_product.id}",
    json={
      "category": "fat",
      "name": "Kebabobs",
      "kcal_per_100g": 150,
      "protein_per_100g": 25,
      "fat_per_100g": 10,
      "carbs_per_100g": 20
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  assert response.json()["name"] == "Kebabobs"

def test_patch_product_valid_data_but_no_changes(client, authenticate_first_user, test_first_product):
  response = client.patch(
    f"/user/products/{test_first_product.id}",
    json={},
    headers=authenticate_first_user
  )

  assert response.status_code == 200

def test_patch_product_unauthorized(client, test_first_product):
  response = client.patch(
    f"/user/products/{test_first_product.id}",
    json={
      "category": "fat",
      "name": "Kebabobs",
      "kcal_per_100g": 150,
      "protein_per_100g": 25,
      "fat_per_100g": 10,
      "carbs_per_100g": 20
    }
  )

  assert response.status_code == 401

def test_patch_product_invalid_data(client, authenticate_first_user, test_first_product):
  response = client.patch(
    f"/user/products/{test_first_product.id}",
    json={
      "category": "Alabama",
      "name": 150,
      "kcal_per_100g": -100,
      "protein_per_100g": 0.5,
      "fat_per_100g": 10,
      "carbs_per_100g": 20000000
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_patch_product_owned_by_other_user(client, authenticate_second_user, test_first_product):
  response = client.patch(
    f"/user/products/{test_first_product.id}",
    json={
      "category": "fat",
      "name": "Kebabobs",
      "kcal_per_100g": 150,
      "protein_per_100g": 25,
      "fat_per_100g": 10,
      "carbs_per_100g": 20
    },
    headers=authenticate_second_user
  )

  assert response.status_code == 404

def test_patch_product_public(client, authenticate_first_user, test_public_product):
  response = client.patch(
    f"/user/products/{test_public_product.id}",
    json={
      "category": "fat",
      "name": "Kebabobs",
      "kcal_per_100g": 150,
      "protein_per_100g": 25,
      "fat_per_100g": 10,
      "carbs_per_100g": 20
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 404

def test_patch_product_does_not_exist(client, authenticate_first_user):
  response = client.patch(
    f"/user/products/0",
    json={
      "category": "fat",
      "name": "Kebabobs",
      "kcal_per_100g": 150,
      "protein_per_100g": 25,
      "fat_per_100g": 10,
      "carbs_per_100g": 20
    },
    headers=authenticate_first_user
  )

  assert response.status_code == 404