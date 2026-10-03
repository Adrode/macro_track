from pydantic import BaseModel
from enum import Enum
from datetime import datetime, timezone

class MealCategory(str, Enum):
  breakfast = "breakfast"
  brunch = "brunch"
  lunch = "lunch"
  dinner = "dinner"
  supper = "supper"

class CreateDiary(BaseModel):
  meal_id: int
  meal_datetime: datetime = datetime.now(timezone.utc)

class DiaryMealProductResponse(BaseModel):
  product_name: str
  kcal_per_100g: float
  protein_per_100g: float
  fat_per_100g: float
  carbs_per_100g: float
  grams: float

class NewDiaryResponse(BaseModel):
  id: int
  meal_name: str
  meal_datetime: datetime

class DiariesResponse(BaseModel):
  id: int
  meal_name: str
  meal_datetime: datetime
  meal_products: list[DiaryMealProductResponse]

class DiariesResponseByCategory(BaseModel):
  id: int
  meal_category: MealCategory
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

class DiarySummaryResponse(BaseModel):
  id: int
  meal_datetime: datetime
  meal_name: str

class DiariesByDateResponse(BaseModel):
  diary: list[DiarySummaryResponse]
  daily_macro_sum: DailyMacroSum
  daily_macro_left: DailyMacroLeft

class PatchDiary(BaseModel):
  meal_id: int | None = None
  meal_datetime: datetime | None = None

class PatchDiaryResponse(BaseModel):
  id: int
  meal_name: str
  meal_datetime: datetime