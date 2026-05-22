from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_me_unauthorized():
  response = client.get("/users/")

  assert response.status_code == 401

def test_get_me_authorized():
  response = client.get("/users/")

  assert response.status_code == 200

  data = response.json()

  assert "id" in data
  assert "email" in data