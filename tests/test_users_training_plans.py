from models.models import TrainingPlan

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
                                {"repetitions": 8},
                            ],
                        },
                    ],
                },
            ],
        },
        headers=authenticate_first_user,
    )

    assert response.status_code == 404


def test_create_training_plan_empty_data(client, authenticate_first_user):
    response = client.post(
        "/user/training-plans/", json={}, headers=authenticate_first_user
    )

    assert response.status_code == 422


def test_get_training_plan_valid_data(
    client, authenticate_first_user, test_training_plan_first_user_1
):
    response = client.get(
        f"/user/training-plans/{test_training_plan_first_user_1.id}",
        headers=authenticate_first_user,
    )

    training_units = response.json()["training_units"]
    training_exercises = [
        exercise for unit in training_units for exercise in unit["training_exercises"]
    ]
    training_exercise_sets = [
        exercise["sets"]
        for unit in training_units
        for exercise in unit["training_exercises"]
    ]

    exercises_names = set()
    for item in training_exercises:
        exercises_names.add(item["exercise_name"])

    assert response.status_code == 200
    assert response.json()["training_plan_name"] == "PPL"
    assert len(training_units) == 3
    assert {"Push ups", "Lat pulldowns", "Leg extensions"}.issubset(exercises_names)
    assert len(training_exercise_sets) == 5


def test_get_training_plan_unauthorized(client, test_training_plan_first_user_1):
    response = client.get(f"/user/training-plans/{test_training_plan_first_user_1.id}")

    assert response.status_code == 401


def test_get_training_plan_does_not_exist(client, authenticate_first_user):
    response = client.get("/user/training-plans/0", headers=authenticate_first_user)

    assert response.status_code == 404


def test_get_training_plan_owned_by_other_user(
    client, authenticate_first_user, test_training_plan_second_user_1
):
    response = client.get(
        f"/user/training-plans/{test_training_plan_second_user_1}",
        headers=authenticate_first_user,
    )

    assert response.status_code == 404


def test_get_training_plan_empty_units(
    client, db_session, authenticate_first_user, test_first_user
):
    new_training_plan = TrainingPlan(
        name="PPL",
        user_id=test_first_user.id,
        source="user"
    )

    db_session.add(new_training_plan)
    db_session.commit()
    db_session.refresh(new_training_plan)
    
    response = client.get(
        f"/user/training-plans/{new_training_plan.id}",
        headers=authenticate_first_user,
    )

    assert response.status_code == 200
    assert response.json()["training_units"] == []


def test_get_training_plans_valid_data(
    client, authenticate_second_user, test_training_plan_second_user_1, test_training_plan_second_user_2
):
    response = client.get(
        "/user/training-plans/",
        headers=authenticate_second_user
    )

    training_plan_names = set()
    for item in response.json():
        training_plan_names.add(item["training_plan_name"])

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert {"FBW", "Leg day"}.issubset(training_plan_names)


def test_get_training_plans_unauthorized(
    client, test_training_plan_second_user_1, test_training_plan_second_user_2
):
    response = client.get(
        "/user/training-plans/"
    )

    assert response.status_code == 401


def test_get_training_plans_does_not_exist(
    client, authenticate_second_user
):
    response = client.get(
        "/user/training-plans/",
        headers=authenticate_second_user
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_training_plans_owned_by_other_user(
    client, authenticate_second_user, test_training_plan_first_user_1
):
    response = client.get(
        "/user/training-plans/",
        headers=authenticate_second_user
    )

    assert response.status_code == 200
    assert response.json() == []