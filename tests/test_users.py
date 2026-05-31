import authentication.short_tokens as auth

def test_get_me_unauthorized(client):
  response = client.get("/users/")

  assert response.status_code == 401

def test_get_me_authorized(client, test_first_user):
  token = auth.create_access_token({
      "sub": test_first_user.email
    })
  response = client.get(
    "/users/",
    headers={"Authorization": f"Bearer {token}"}
  )

  data = response.json()

  assert response.status_code == 200
  assert "email" in data
  assert "id" in data
  
def test_patch_me_unauthorized(client, test_first_user):
  response = client.patch(
    "/users/",
    json={"username": test_first_user.username}
  )

  assert response.status_code == 401

def test_patch_me_authorized(client, test_first_user):
  token = auth.create_access_token({
      "sub": test_first_user.email
    })
  response = client.patch(
    "/users/",
    json={"username": "Adrian"},
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response.status_code == 200
  
  response2 = client.get(
    "/users/",
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response2.json()["username"] == "Adrian"

def test_patch_me_invalid_email(client, test_first_user):
  token = auth.create_access_token({
      "sub": test_first_user.email
    })
  response = client.patch(
    "/users/",
    json={"email": "kekw2"},
    headers={"Authorization": f"Bearer {token}"}
  )

  assert response.status_code == 422