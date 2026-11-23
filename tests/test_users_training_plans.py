def test_create_training_plan_valid_data(
    client,
    authenticate_first_user,
    test_exercise_first_user_1,
    test_exercise_first_user_2,
):
    response = client.post(
        "/user/training-plans/",
        json={
            "training_plan_name": "New TP",
            "training_units": [
                {
                    "training_unit_name": "Unit 1",
                    "training_unit_description": "Unit 1 description",
                    "training_exercises": [
                        {
                            "exercise_id": test_exercise_first_user_1.id,
                            "sets": [
                                {
                                    "repetitions": 10,
                                },
                                {"repetitions": 8},
                            ],
                        },
                        {
                            "exercise_id": test_exercise_first_user_2.id,
                            "sets": [
                                {
                                    "repetitions": 6,
                                },
                                {"repetitions": 6},
                            ],
                        },
                    ],
                },
                {
                    "training_unit_name": "Unit 2",
                    "training_unit_description": "Unit 2 description",
                    "training_exercises": [
                        {
                            "exercise_id": test_exercise_first_user_2.id,
                            "sets": [
                                {"repetitions": 20},
                                {"repetitions": 18},
                                {"repetitions": 16},
                            ],
                        }
                    ],
                },
            ],
        },
        headers=authenticate_first_user,
    )

    assert response.status_code == 200
    assert response.json()["training_plan_name"] == "New TP"
    assert response.json()["source"] == "user"


def test_create_training_plan_invalid_data(
    client,
    authenticate_first_user,
    test_exercise_first_user_1,
):
    response = client.post(
        "/user/training-plans/",
        json={"training_plan_name": 15},
        headers=authenticate_first_user,
    )

    assert response.status_code == 422


def test_create_training_plan_empty_training_units(
    client,
    authenticate_first_user,
    test_exercise_first_user_1,
):
    response = client.post(
        "/user/training-plans/",
        json={"training_plan_name": "New TP", "training_units": []},
        headers=authenticate_first_user,
    )

    assert response.status_code == 200


def test_create_training_plan_unauthorized(client):
    response = client.post(
        "/user/training-plans/",
        json={"training_plan_name": "New TP", "training_units": []},
    )

    assert response.status_code == 401


def test_create_training_plan_exercise_owned_by_other_user(
    client, authenticate_first_user
):
    response = client.post(
        "/user/training-plans/",
        json={
            "training_plan_name": "New TP",
            "training_units": [
                {
                    "training_unit_name": "Unit 1",
                    "training_unit_description": "Unit 1 description",
                    "training_exercises": [
                        {
                            "exercise_id": 0,
                            "sets": [
                                {
                                    "repetitions": 10,
                                },
                                {
                                    "repetitions": 8
                                },
                            ],
                        },
                    ],
                },
            ],
        },
        headers=authenticate_first_user
    )

    assert response.status_code == 404


def test_create_training_plan_empty_data(
    client, authenticate_first_user
):
    response = client.post(
        "/user/training-plans/",
        json={},
        headers=authenticate_first_user
    )

    assert response.status_code == 422
