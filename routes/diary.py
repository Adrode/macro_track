from fastapi import APIRouter
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from utils.dependencies import session_dependency
from utils.exceptions import not_found_exc, bad_request_exc
from schemas import diary_schemas
from models import models

router = APIRouter()

@router.post("/", response_model=diary_schemas.DiaryResponse)
def post_diary(data: diary_schemas.CreateDiary, session: session_dependency):
  try:
    new_diary = models.UserDiary(
      user_id=data.user_id,
      meal_id=data.meal_id,
      meal_datetime=data.meal_datetime
    )

    session.add(new_diary)
    session.flush()

    if new_diary.meal.user_id != data.user_id:
      raise bad_request_exc

    session.commit()
    session.refresh(new_diary)
    return new_diary
  except IntegrityError:
    raise bad_request_exc
  
@router.get("/{user_id}/{date}")
def get_diary_by_date(user_id: int, date: datetime, session: session_dependency):
  diary = session.scalars(select(models.UserDiary).where(
    models.UserDiary.user_id == user_id,
    func.date(models.UserDiary.meal_datetime) == date.date()
    )
  ).all()
  user = session.scalars(select(models.User).where(models.User.id == user_id)).first()

  if not diary:
    raise not_found_exc
  
  response = []
  daily_macro = {
    "sum_of_kcal": 0,
    "sum_of_protein": 0,
    "sum_of_fat": 0,
    "sum_of_carbs": 0
  }

  for item in diary:
    response.append({
      "id": item.id,
      "meal_datetime": item.meal_datetime,
      "user_id": item.user_id,
      "meal_id": item.meal_id,
      "meal_name": item.meal.name
    })
    
    for i in item.meal.meals_products:
      daily_macro["sum_of_kcal"] += i.product.kcal_per_100g * (i.grams / 100)
      daily_macro["sum_of_protein"] += i.product.protein_per_100g * (i.grams / 100)
      daily_macro["sum_of_fat"] += i.product.fat_per_100g * (i.grams / 100)
      daily_macro["sum_of_carbs"] += i.product.carbs_per_100g * (i.grams / 100)

  daily_macro_left = {
    "kcal_left": user.kcal_daily_goal - daily_macro["sum_of_kcal"],
    "protein_left": user.protein_daily_goal - daily_macro["sum_of_protein"],
    "fat_left": user.fat_daily_goal - daily_macro["sum_of_fat"],
    "carbs_left": user.carbs_daily_goal - daily_macro["sum_of_carbs"]
  }

  return {
    "diary": response,
    "daily_macro_sum": daily_macro,
    "daily_macro_left": daily_macro_left
  }