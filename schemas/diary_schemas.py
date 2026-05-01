from pydantic import BaseModel
from datetime import datetime, timezone

class CreateDiary(BaseModel):
  user_id: int
  meal_id: int
  meal_datetime: datetime = datetime.now(timezone.utc)

class DiaryResponse(BaseModel):
  user_id: int
  meal_id: int
  meal_datetime: datetime