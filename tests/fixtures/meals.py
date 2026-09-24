import pytest
from models.models import Meal, MealProduct

@pytest.fixture()
def test_meal_first_user_1(
  db_session,
  test_first_user,
  test_first_product,
  test_public_product
):
  meal = Meal(
    category="breakfast",
    name="Oatmeal",
    user_id=test_first_user.id
  )

  db_session.add(meal)
  db_session.flush()
  
  meal_product1 = MealProduct(
    meal_id=meal.id,
    product_id=test_first_product.id,
    grams=150
  )
  meal_product2 = MealProduct(
    meal_id=meal.id,
    product_id=test_public_product.id,
    grams=200
  )

  db_session.add(meal_product1)
  db_session.add(meal_product2)
  db_session.commit()
  db_session.refresh(meal)

  return meal

@pytest.fixture()
def test_meal_second_user_1(
  db_session,
  test_second_user,
  test_second_product
):
  meal = Meal(
    category="dinner",
    name="Kasza manna damn",
    user_id=test_second_user.id
  )

  db_session.add(meal)
  db_session.flush()

  meal_product = MealProduct(
    meal_id=meal.id,
    product_id=test_second_product.id,
    grams=80
  )

  db_session.add(meal_product)
  db_session.commit()
  db_session.refresh(meal)

  return meal

@pytest.fixture()
def test_meal_second_user_2(
  db_session,
  test_second_user,
  test_public_product
):
  meal = Meal(
    category="supper",
    name="Pijany dzik",
    is_active=False,
    user_id=test_second_user.id
  )

  db_session.add(meal)
  db_session.flush()

  meal_product = MealProduct(
    meal_id=meal.id,
    product_id=test_public_product.id,
    grams=350
  )

  db_session.add(meal_product)
  db_session.commit()
  db_session.refresh(meal)

  return meal