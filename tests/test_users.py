import authentication.short_tokens as auth

def test_get_me_unauthorized(client):
  response = client.get("/users/")

  assert response.status_code == 401

def test_get_me_authorized(client):
  token = auth.create_access_token({
      "sub": "adrian@gmail.com"
    })
  response = client.get(
    "/users/",
    headers={
      "Authorization": f"Bearer {token}"
    }
    )

  data = response.json()

  assert response.status_code == 200
  assert "email" in data
  assert "id" in data
  
def test_patch_me_unauthorized(client):
  response = client.patch(
    "/users/",
    json={"username": "Adison"}
  )

  assert response.status_code == 401

def test_patch_me_authorized(client):
  token = auth.create_access_token({
      "sub": "adrian@gmail.com"
    })
  response = client.patch(
    "/users/",
    json={"username": "Adison"},
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response.status_code == 200
  
  response2 = client.get(
    "/users/",
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response2.json()["username"] == "Adison"

def test_patch_me_invalid_email(client):
  token = auth.create_access_token({
      "sub": "adrian@gmail.com"
    })
  response = client.patch(
    "/users/",
    json={"email": "kekw2"},
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response.status_code == 422