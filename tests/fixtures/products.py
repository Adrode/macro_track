import pytest
from models.models import Product

@pytest.fixture()
def test_public_product(db_session):
  product = Product(
    category="carbs",
    name="Baton",
    kcal_per_100g=150,
    protein_per_100g=20,
    fat_per_100g=5,
    carbs_per_100g=45,
    user_id=None
  )

  db_session.add(product)
  db_session.commit()
  db_session.refresh(product)

  return product

@pytest.fixture()
def test_first_product(db_session, test_first_user):
  product = Product(
    category="carbs",
    name="Pierogies",
    kcal_per_100g=150,
    protein_per_100g=20,
    fat_per_100g=5,
    carbs_per_100g=45,
    user_id=test_first_user.id
  )

  db_session.add(product)
  db_session.commit()
  db_session.refresh(product)

  return product

@pytest.fixture()
def test_second_product(db_session, test_second_user):
  product = Product(
    category="carbs",
    name="Macaronis",
    kcal_per_100g=350,
    protein_per_100g=10,
    fat_per_100g=10,
    carbs_per_100g=60,
    user_id=test_second_user.id
  )

  db_session.add(product)
  db_session.commit()
  db_session.refresh(product)

  return product