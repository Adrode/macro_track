from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from utils.dependencies import session_dependency
from utils.exceptions import bad_request_exc, not_found_exc
from models import models
from schemas import meal_schemas

router = APIRouter()

@router.post("/", response_model=meal_schemas.MealResponse)
def add_meal(
  data: meal_schemas.CreateMealWithProducts,
  session: session_dependency
):
  try:
    meal = models.Meal(
      category=data.category,
      name=data.name,
      user_id=data.user_id
    )
    
    session.add(meal)
    session.flush()

    meal_products_list = []

    for item in data.meal_products:
      meal_products_list.append(
        models.MealProduct(
          meal_id=meal.id,
          product_id=item.product_id,
          grams=item.grams
        )
      )

    for item in meal_products_list:
      session.add(item)
    
    session.commit()
    session.refresh(meal)
    return meal

  except IntegrityError:
    raise bad_request_exc
  
@router.delete("/{id}")
def delete_meal(id: int, session: session_dependency):
  meal = session.scalars(select(models.Meal).where(models.Meal.id == id)).first()

  if not meal:
    raise not_found_exc
  
  session.delete(meal)
  session.commit()
  return {"detail": f"Meal id {meal.id} removed"}

@router.patch("/{id}", response_model=meal_schemas.MealResponse)
def patch_meal(
  id: int,
  data: meal_schemas.PatchMealWithProducts,
  session: session_dependency
):
  meal = session.scalars(select(models.Meal).where(models.Meal.id == id)).first()

  if not meal:
    raise not_found_exc
  
  if data.meal_products:
    for item in meal.meals_products:
      session.delete(item)
    
    session.flush()

    for item in data.meal_products:
      session.add(
        models.MealProduct(
          meal_id=meal.id,
          product_id=item.product_id,
          grams=item.grams
        )
      )

  patch_data = data.model_dump(exclude_unset=True, exclude={"meal_products"})
  for key, value in patch_data.items():
    setattr(meal, key, value)

  session.commit()
  session.refresh(meal)
  return meal

@router.get("/{id}", response_model=meal_schemas.MealWithProductsResponse)
def get_meal(id: int, session: session_dependency):
  meal = session.scalars(select(models.Meal).where(models.Meal.id == id)).first()

  if not meal:
    raise not_found_exc
  
  products_list = []
  macro_dict = {
    "sum_of_kcal": 0,
    "sum_of_protein": 0,
    "sum_of_fat": 0,
    "sum_of_carbs": 0
  }

  for item in meal.meals_products:
    products_list.append({
      "product_name": item.product.name,
      "grams": item.grams
    })
    macro_dict["sum_of_kcal"] += item.product.kcal_per_100g * (item.grams / 100)
    macro_dict["sum_of_protein"] += item.product.protein_per_100g * (item.grams / 100)
    macro_dict["sum_of_fat"] += item.product.fat_per_100g * (item.grams / 100)
    macro_dict["sum_of_carbs"] += item.product.carbs_per_100g * (item.grams / 100)
  
  response = {
    "category": meal.category,
    "name": meal.name,
    "user_id": meal.user_id,
    "user_username": meal.user.username,
    "products": products_list,
    "macro": macro_dict
  }

  return response

@router.get("/", response_model=list[meal_schemas.AllMealsByUserReponse])
def get_all_meals(user_id: int, session: session_dependency):
  meals = session.scalars(select(models.Meal).where(models.Meal.user_id == user_id)).all()

  if not meals:
    raise not_found_exc

  macro_dict = {
    "sum_of_kcal": 0,
    "sum_of_protein": 0,
    "sum_of_fat": 0,
    "sum_of_carbs": 0
  }

  response = []

  for meal in meals:
    for item in meal.meals_products:
      macro_dict["sum_of_kcal"] += item.product.kcal_per_100g * (item.grams / 100)
      macro_dict["sum_of_protein"] += item.product.protein_per_100g * (item.grams / 100)
      macro_dict["sum_of_fat"] += item.product.fat_per_100g * (item.grams / 100)
      macro_dict["sum_of_carbs"] += item.product.carbs_per_100g * (item.grams / 100)

    response.append({
      "name": meal.name,
      "category": meal.category,
      "macro": macro_dict
    })

    macro_dict = {
    "sum_of_kcal": 0,
    "sum_of_protein": 0,
    "sum_of_fat": 0,
    "sum_of_carbs": 0
    }
  
  return response