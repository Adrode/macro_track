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
    meal = session.scalars(select(models.Meal).where(models.Meal.id == data.meal_id)).first()

    if not meal:
      raise not_authorized_token_exc("Not authorized")

    new_diary = models.DiaryEntry(
      user_id=current_user.id,
      meal_category=meal.category,
      meal_name=meal.name,
      meal_datetime=data.meal_datetime
    )

    session.add(new_diary)
    session.flush()

    for item in meal.meal_products:
      new_diary_meal_product = models.DiaryMealProduct(
        diary_id=new_diary.id,
        product_name=item.product.name,
        kcal_per_100g=item.product.kcal_per_100g,
        protein_per_100g=item.product.protein_per_100g,
        fat_per_100g=item.product.fat_per_100g,
        carbs_per_100g=item.product.carbs_per_100g,
        grams=item.grams
      )
      session.add(new_diary_meal_product)

    session.commit()
    session.refresh(new_diary)

    response = {
      "id": new_diary.id,
      "meal_name": new_diary.meal_name,
      "meal_datetime": new_diary.meal_datetime
    }
    return response
  
  except IntegrityError:
    raise bad_request_exc
  
@router.get("/entry/{id}", response_model=diary_schemas.DiariesResponse)
def get_diary_by_id(
  id: int,
  session: session_dependency,
  current_user: current_user_dependency
):
  diary = session.scalars(select(models.DiaryEntry).where(models.DiaryEntry.id == id)).first()

  if not diary or diary.user_id != current_user.id:
    raise not_authorized_token_exc("Diary not authorized")

  meal_products = []
  for item in diary.diary_meal_products:
    meal_products.append({
      "product_name": item.product_name,
      "kcal_per_100g": item.kcal_per_100g,
      "protein_per_100g": item.protein_per_100g,
      "fat_per_100g": item.fat_per_100g,
      "carbs_per_100g": item.carbs_per_100g,
      "grams": item.grams
    })
  
  response = {
    "id": diary.id,
    "meal_name": diary.meal_name,
    "meal_datetime": diary.meal_datetime,
    "meal_products": meal_products
  }

  return response

@router.get("/{date}", response_model=diary_schemas.DiariesByDateResponse)
def get_diaries_by_date(
  date: datetime,
  session: session_dependency,
  current_user: current_user_dependency
):
  diaries = session.scalars(select(models.DiaryEntry).where(
      models.DiaryEntry.user_id == current_user.id,
      func.date(models.DiaryEntry.meal_datetime) == date.date()
    )
  ).all()

  if not diaries:
    raise not_authorized_token_exc("Not authorized")
  
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
      "meal_name": item.meal_name
    })
    
    for i in item.diary_meal_products:
      daily_macro["sum_of_kcal"] += i.kcal_per_100g * (i.grams / 100)
      daily_macro["sum_of_protein"] += i.protein_per_100g * (i.grams / 100)
      daily_macro["sum_of_fat"] += i.fat_per_100g * (i.grams / 100)
      daily_macro["sum_of_carbs"] += i.carbs_per_100g * (i.grams / 100)

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
    raise not_authorized_token_exc("Diaries not found")
  
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
    raise not_authorized_token_exc("Diaries not found")
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
    raise not_authorized_token_exc("Diaries not found")
  if diary.user_id != current_user.id:
    raise not_authorized_token_exc("Not authorized")
  
  if data.meal_id:
    meal = session.scalars(select(models.Meal).where(models.Meal.id == data.meal_id)).first()
    if meal.user_id != current_user.id:
      raise not_authorized_token_exc("Meal not authorized")
    if meal.is_active == False:
      raise bad_request_exc
  
  to_patch = data.model_dump(exclude_unset=True)

  for key, value in to_patch.items():
    setattr(diary, key, value)

  session.commit()
  session.refresh(diary)
  return diary