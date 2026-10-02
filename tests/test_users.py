import authentication.short_tokens as auth

def test_get_me_authorized(client, test_first_user, authenticate_first_user):
  token = auth.create_access_token({
      "sub": test_first_user.email,
      "role": "user"
    })
  response = client.get(
    "/user/",
    headers=authenticate_first_user
  )

  data = response.json()

  assert response.status_code == 200
  assert "email" in data
  assert "id" in data

def test_get_me_unauthorized(client):
  response = client.get("/user/")

  assert response.status_code == 401
  
def test_patch_me_unauthorized(client, test_first_user):
  response = client.patch(
    "/user/",
    json={"username": test_first_user.username}
  )

  assert response.status_code == 401

def test_patch_me_authorized(client, authenticate_first_user):
  response = client.patch(
    "/user/",
    json={"username": "Adrian"},
    headers=authenticate_first_user
  )

  assert response.status_code == 200
  
  response2 = client.get(
    "/user/",
    headers=authenticate_first_user
  )

  assert response2.json()["username"] == "Adrian"

def test_patch_me_invalid_email(client, authenticate_first_user):
  response = client.patch(
    "/user/",
    json={"email": "kekw2"},
    headers=authenticate_first_user
  )

  assert response.status_code == 422

def test_patch_me_email_already_taken(client, test_second_user, authenticate_first_user):
  response = client.patch(
    "/user/",
    json={"email": test_second_user.email},
    headers=authenticate_first_user
  )

  assert response.status_code == 400

def test_patch_me_username_already_taken(client, test_second_user, authenticate_first_user):
  response = client.patch(
    "/user/",
    json={"username": test_second_user.username},
    headers=authenticate_first_user
  )

  assert response.status_code == 400