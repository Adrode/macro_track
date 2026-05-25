from fastapi.testclient import TestClient
from main import app
import authentication.short_tokens as auth

client = TestClient(app)

def test_get_me_unauthorized():
  response = client.get("/users/")

  assert response.status_code == 401

def test_get_me_authorized():
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
  