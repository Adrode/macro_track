from fastapi import APIRouter
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from utils.dependencies import session_dependency, current_user_dependency
from utils.exceptions import not_found_exc, bad_request_exc, not_authorized_token_exc
from schemas import diary_schemas
from models import models

router = APIRouter()

@router.post("/", response_model=diary_schemas.NewDiaryResponse)
def post_diary(
  data: diary_schemas.CreateDiary,
  session: session_dependency,
  current_user: current_user_dependency
):
  try:
    new_diary = models.UserDiary(
      user_id=current_user.id,
      meal_id=data.meal_id,
      meal_datetime=data.meal_datetime
    )

    session.add(new_diary)
    session.flush()

    if new_diary.meal.user_id != current_user.id:
      raise not_authorized_token_exc("Not authorized")
    
    if new_diary.meal.is_active == False:
      raise bad_request_exc

    session.commit()
    session.refresh(new_diary)
    return new_diary
  except IntegrityError:
    raise bad_request_exc
  
@router.get("/entry/{id}", response_model=diary_schemas.DiariesResponse)
def get_diary_by_id(
  id: int,
  session: session_dependency,
  current_user: current_user_dependency
):
  diary = session.scalars(select(models.UserDiary).where(models.UserDiary.id == id)).first()

  if not diary:
    raise not_found_exc
  if diary.user_id != current_user.id:
    raise not_authorized_token_exc("Not authorized")
  
  response = {
    "id": diary.id,
    "meal_id": diary.meal_id,
    "meal_name": diary.meal.name,
    "meal_datetime": diary.meal_datetime
  }

  return response

@router.get("/{date}", response_model=diary_schemas.DiariesByDateResponse)
def get_diaries_by_date(
  date: datetime,
  session: session_dependency,
  current_user: current_user_dependency
):
  diaries = session.scalars(select(models.UserDiary).where(
    models.UserDiary.user_id == current_user.id,
    func.date(models.UserDiary.meal_datetime) == date.date()
    )
  ).all()

  if not diaries:
    raise not_found_exc
  
  response = []
  daily_macro = {
    "sum_of_kcal": 0,
    "sum_of_protein": 0,
    "sum_of_fat": 0,
    "sum_of_carbs": 0
  }

  for item in diaries:
    response.append({
      "id": item.id,
      "meal_datetime": item.meal_datetime,
      "meal_id": item.meal_id,
      "meal_name": item.meal.name
    })
    
    for i in item.meal.meals_products:
      daily_macro["sum_of_kcal"] += i.product.kcal_per_100g * (i.grams / 100)
      daily_macro["sum_of_protein"] += i.product.protein_per_100g * (i.grams / 100)
      daily_macro["sum_of_fat"] += i.product.fat_per_100g * (i.grams / 100)
      daily_macro["sum_of_carbs"] += i.product.carbs_per_100g * (i.grams / 100)

  daily_macro_left = {
    "kcal_left": current_user.kcal_daily_goal - daily_macro["sum_of_kcal"],
    "protein_left": current_user.protein_daily_goal - daily_macro["sum_of_protein"],
    "fat_left": current_user.fat_daily_goal - daily_macro["sum_of_fat"],
    "carbs_left": current_user.carbs_daily_goal - daily_macro["sum_of_carbs"]
  }

  return {
    "diary": response,
    "daily_macro_sum": daily_macro,
    "daily_macro_left": daily_macro_left
  }

@router.get("/", response_model=list[diary_schemas.DiariesResponse])
def get_all_diaries(
  session: session_dependency,
  current_user: current_user_dependency
):
  diaries = session.scalars(select(models.UserDiary).where(models.UserDiary.user_id == current_user.id)).all()

  if not diaries:
    raise not_found_exc
  
  response = []

  for item in diaries:
    response.append({
      "id": item.id,
      "meal_id": item.meal_id,
      "meal_name": item.meal.name,
      "meal_datetime": item.meal_datetime
    })

  return response

@router.delete("/{id}")
def delete_diary(
  id: int,
  session: session_dependency,
  current_user: current_user_dependency  
):
  diary = session.scalars(select(models.UserDiary).where(models.UserDiary.id == id)).first()

  if not diary:
    raise not_found_exc
  if diary.user_id != current_user.id:
    raise not_authorized_token_exc("Not authorized")
  
  session.delete(diary)
  session.commit()
  return {"detail": f"Diary by ID {diary.id} removed from database"}

@router.patch("/{id}", response_model=diary_schemas.PatchDiaryResponse)
def patch_diary(
  id: int,
  data: diary_schemas.PatchDiary,
  session: session_dependency,
  current_user: current_user_dependency
):
  diary = session.scalars(select(models.UserDiary).where(models.UserDiary.id == id)).first()
  
  if not diary:
    raise not_found_exc
  if diary.user_id != current_user.id:
    raise not_authorized_token_exc("Not authorized")
  
  if data.meal_id:
    meal = session.scalars(select(models.Meal).where(models.Meal.id == data.meal_id)).first()
    if meal.user_id != current_user.id:
      raise not_authorized_token_exc("Not authorized")
    if meal.is_active == False:
      raise bad_request_exc
  
  to_patch = data.model_dump(exclude_unset=True)

  for key, value in to_patch.items():
    setattr(diary, key, value)

  session.commit()
  session.refresh(diary)
  return diary