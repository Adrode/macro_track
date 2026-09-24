import pytest
from datetime import datetime
from models.models import DiaryEntry, DiaryMealProduct

@pytest.fixture()
def test_diary_first_user_1(
  db_session,
  test_first_user,
  test_meal_first_user_1
):
  diary = DiaryEntry(
    user_id=test_first_user.id,
    meal_id=test_meal_first_user_1.id,
    meal_datetime=datetime(2026, 5, 6, 8, 30)
  )

  db_session.add(diary)
  db_session.commit()
  db_session.refresh(diary)

  return diary

@pytest.fixture()
def test_diary_second_user_1(
  db_session,
  test_second_user,
  test_meal_second_user_1
):
  diary = DiaryEntry(
    user_id=test_second_user.id,
    meal_id=test_meal_second_user_1.id,
    meal_datetime=datetime(2026, 5, 10, 8, 30)
  )

  db_session.add(diary)
  db_session.commit()
  db_session.refresh(diary)

  return diary

@pytest.fixture()
def test_diary_second_user_2(
  db_session,
  test_second_user,
  test_meal_second_user_2
):
  diary = DiaryEntry(
    user_id=test_second_user.id,
    meal_id=test_meal_second_user_2.id,
    meal_datetime=datetime(2026, 5, 10, 9, 30)
  )

  db_session.add(diary)
  db_session.commit()
  db_session.refresh(diary)

  return diary