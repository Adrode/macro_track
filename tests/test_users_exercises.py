def test_create_exercise_valid_data(client, authenticate_first_user):
    response = client.post(
        "/user/exercises/",
        json={"name": "Hip thrusts", "main_muscles": ["glutes"], "side_muscles": []},
        headers=authenticate_first_user,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Hip thrusts"

    response = client.get(
        "/user/exercises/",
        headers=authenticate_first_user
    )
    
    assert len(response.json()) == 1


def test_create_exercise_invalid_data(client, authenticate_first_user):
    response = client.post(
        "/user/exercises/",
        json={"name": 5, "main_muscles": 10, "side_muscles": "glutes"},
        headers=authenticate_first_user,
    )

    assert response.status_code == 422


def test_create_exercise_unauthorized(client):
    response = client.post(
        "/user/exercises/",
        json={"name": "Cool exercise", "main_muscles": ["biceps"], "side_muscles": ["triceps"]},
    )

    assert response.status_code == 401

def test_