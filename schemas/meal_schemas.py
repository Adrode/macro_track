from enum import Enum
from pydantic import BaseModel

class MealCategory(str, Enum):
  breakfast = "breakfast"
  brunch = "brunch"
  lunch = "lunch"
  dinner = "dinner"
  supper = "supper"

class MealProducts(BaseModel):
  product_id: int
  grams: int

class CreateMealWithProducts(BaseModel):
  category: MealCategory
  name: str
  user_id: int
  meal_products: list[MealProducts]