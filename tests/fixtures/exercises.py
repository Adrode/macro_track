import pytest
from models.models import Exercise

@pytest.fixture()
def test_exercise_first_user_1(
  db_session,
  test_first_user
):
  exercise = Exercise(
    name = "Push ups",
    main_muscles = ["chest", "triceps"],
    side_muscles = ["front_delts"],
    description = "Basic push-ups",
    user_id = test_first_user.id,
    trainer_id = None
  )

  db_session.add(exercise)
  db_session.commit()
  db_session.refresh(exercise)

  return exercise

@pytest.fixture()
def test_exercise_second_user_1(
  db_session,
  test_second_user
):
  exercise = Exercise(
    name = "Pull ups",
    main_muscles = ["lats", "biceps"],
    side_muscles = [],
    user_id = test_second_user.id,
    trainer_id = None
  )

  db_session.add(exercise)
  db_session.commit()
  db_session.refresh(exercise)

  return exercise

@pytest.fixture()
def test_exercise_second_user_2(
  db_session,
  test_second_user
):
  exercise = Exercise(
    name = "Squats",
    main_muscles = ["glutes", "hamstrings"],
    side_muscles = ["quads"],
    user_id = test_second_user.id,
    trainer_id = None
  )

  db_session.add(exercise)
  db_session.commit()
  db_session.refresh(exercise)

  return exercise

@pytest.fixture()
def test_exercise_public(
  db_session
):
  exercise = Exercise(
    name = "Deadlift",
    main_muscles = ["hamstrings", "glutes", "lower_back", "upper_back"],
    side_muscles = ["quads"],
    user_id = None,
    trainer_id = None
  )

  db_session.add(exercise)
  db_session.commit()
  db_session.refresh(exercise)

  return exercise