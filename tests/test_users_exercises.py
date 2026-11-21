def test_create_exercise_valid_data(client, authenticate_first_user):
    response = client.post(
        "/user/exercises/",
        json={"name": "Hip thrusts", "main_muscles": ["glutes"], "side_muscles": []},
        headers=authenticate_first_user,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Hip thrusts"

    response = client.get("/user/exercises/", headers=authenticate_first_user)

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
        json={
            "name": "Cool exercise",
            "main_muscles": ["biceps"],
            "side_muscles": ["triceps"],
        },
    )

    assert response.status_code == 401


def test_get_exercise_valid_data(
    client, authenticate_first_user, test_exercise_first_user_1
):
    response = client.get(
        f"/user/exercises/{test_exercise_first_user_1.id}",
        headers=authenticate_first_user,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Push ups"


def test_get_exercise_check_public(
    client, authenticate_first_user, test_exercise_public
):
    response = client.get(
        f"/user/exercises/{test_exercise_public.id}", headers=authenticate_first_user
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Deadlift"


def test_get_exercise_does_not_exist(client, authenticate_first_user):
    response = client.get(
        "/user/exercises/0",
        headers=authenticate_first_user,
    )

    assert response.status_code == 404


def test_get_exercise_owned_by_other_user(
    client, authenticate_first_user, test_exercise_second_user_1
):
    response = client.get(
        f"/user/exercises/{test_exercise_second_user_1.id}",
        headers=authenticate_first_user,
    )

    assert response.status_code == 404

    response = client.get("/user/exercises/", headers=authenticate_first_user)

    assert response.json() == []


def test_get_exercises_valid_data(
    client,
    authenticate_second_user,
    test_exercise_second_user_1,
    test_exercise_second_user_2,
    test_exercise_public,
):
    response = client.get("/user/exercises/", headers=authenticate_second_user)

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_exercises_no_items(client, authenticate_second_user):
    response = client.get("/user/exercises/", headers=authenticate_second_user)

    assert response.status_code == 200
    assert response.json() == []


def test_get_exercises_no_items(client, authenticate_second_user):
    response = client.get("/user/exercises/", headers=authenticate_second_user)

    assert response.status_code == 200
    assert response.json() == []


def test_get_exercises_unauthorized(client):
    response = client.get("/user/exercises/")

    assert response.status_code == 401


def test_delete_exercise_valid_data(client, authenticate_second_user, test_exercise_second_user_1, test_exercise_second_user_2):
    response = client.get(
        f"/user/exercises/",
        headers=authenticate_second_user
    )

    assert response.status_code == 200
    assert len(response.json()) == 2
    
    response = client.delete(
        f"/user/exercises/{test_exercise_second_user_1.id}",
        headers=authenticate_second_user
    )

    assert response.status_code == 200

    response = client.get(
        f"/user/exercises/",
        headers=authenticate_second_user
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_exercise_other_user(client, authenticate_first_user, test_exercise_second_user_1):
    response = client.delete(
        f"/user/exercises/{test_exercise_second_user_1.id}",
        headers=authenticate_first_user
    )

    assert response.status_code == 404


def test_delete_exercise_does_not_exist(client, authenticate_second_user, test_exercise_second_user_1):
    response = client.delete(
        "/user/exercises/0",
        headers=authenticate_second_user
    )

    assert response.status_code == 404


def test_delete_exercise_unauthorized(client, test_exercise_first_user_1):
    response = client.delete(
        f"/user/exercises/{test_exercise_first_user_1.id}"
    )

    assert response.status_code == 401


def test_delete_exercise_public(client, authenticate_first_user, test_exercise_public):
    response = client.delete(
        f"/user/exercises/{test_exercise_public.id}",
        headers=authenticate_first_user
    )

    assert response.status_code == 404

    response = client.get(
        "/user/exercises/",
        headers=authenticate_first_user
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Deadlift"


def test_patch_exercise_valid_data(client, authenticate_first_user, test_exercise_first_user_1):
    response = client.patch(
        f"/user/exercises/{test_exercise_first_user_1.id}",
        json={
            "name": "Kappa",
            "side_muslces": ["biceps"],
            "description": None
        },
        headers=authenticate_first_user
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Kappa"
    assert response.json()["description"] == None
    assert response.json()["main_muscles"] == ["chest", "triceps"]


def test_patch_exercise_no_data(client, authenticate_first_user, test_exercise_first_user_1):
    response1 = client.patch(
        f"/user/exercises/{test_exercise_first_user_1.id}",
        json={},
        headers=authenticate_first_user
    )

    assert response1.status_code == 200
    assert response1.json()["name"] == "Push ups"

    response2 = client.get(
        f"/user/exercises/{test_exercise_first_user_1.id}",
        headers=authenticate_first_user
    )

    assert response2.status_code == 200
    assert response2.json()["name"] == "Push ups"

    assert response1.json() == response2.json()


def test_patch_exercise_invalid_data(client, authenticate_first_user, test_exercise_first_user_1):
    response1 = client.patch(
        f"/user/exercises/{test_exercise_first_user_1.id}",
        json={
            "name": 15,
            "age": "200"
        },
        headers=authenticate_first_user
    )

    assert response1.status_code == 422


def test_patch_exercise_unauthorized(client, test_exercise_first_user_1):
    response1 = client.patch(
        f"/user/exercises/{test_exercise_first_user_1.id}",
        json={
            "name": "Kappa",
            "side_muslces": ["biceps"]
        }
    )

    assert response1.status_code == 401


def test_patch_exercise_owned_by_other_user(client, authenticate_second_user, test_exercise_first_user_1):
    response1 = client.patch(
        f"/user/exercises/{test_exercise_first_user_1.id}",
        json={
            "name": "Kappa",
            "side_muslces": ["biceps"]
        },
        headers=authenticate_second_user
    )

    assert response1.status_code == 404