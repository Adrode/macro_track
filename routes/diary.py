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

  if not diary:
    raise not_found_exc

  return diary