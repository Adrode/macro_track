from pydantic import BaseModel
from datetime import datetime, timezone

class CreateDiary(BaseModel):
  meal_id: int
  meal_datetime: datetime = datetime.now(timezone.utc)

class NewDiaryResponse(BaseModel):
  id: int
  meal_id: int
  meal_datetime: datetime

class DiariesResponse(BaseModel):
  id: int
  meal_id: int
  meal_name: str
  meal_datetime: datetime

class DailyMacroSum(BaseModel):
  sum_of_kcal: float
  sum_of_protein: float
  sum_of_fat: float
  sum_of_carbs: float

class DailyMacroLeft(BaseModel):
  kcal_left: float
  protein_left: float
  fat_left: float
  carbs_left: float

class DiariesByDateResponse(BaseModel):
  diary: list[DiariesResponse]
  daily_macro_sum: DailyMacroSum
  daily_macro_left: DailyMacroLeft

class PatchDiary(BaseModel):
  meal_id: int | None = None
  meal_datetime: datetime | None = None

class PatchDiaryResponse(BaseModel):
  id: int
  meal_id: int
  meal_datetime: datetime