import pytest
from uuid import uuid4
from models.models import User
from authentication.pwd_hash import hash_password

@pytest.fixture()
def test_first_user(db_session):
  password = "fakehash"

  user = User(
    email=f"adrian-{uuid4()}@gmail.com",
    username="Adrian",
    hashed_password=hash_password(password),
    kcal_daily_goal=2000,
    protein_daily_goal=100,
    fat_daily_goal=70,
    carbs_daily_goal=250
  )

  db_session.add(user)
  db_session.commit()
  db_session.refresh(user)

  user.plain_password = password

  return user

@pytest.fixture()
def test_second_user(db_session):
  password = "hashfake"

  user = User(
    email=f"second-{uuid4()}@gmail.com",
    username="Second",
    hashed_password=hash_password(password),
    kcal_daily_goal=3000,
    protein_daily_goal=150,
    fat_daily_goal=70,
    carbs_daily_goal=300
  )

  db_session.add(user)
  db_session.commit()
  db_session.refresh(user)

  user.plain_password = password

  return user