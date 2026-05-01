from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from utils.dependencies import session_dependency
from utils.exceptions import bad_request_exc
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