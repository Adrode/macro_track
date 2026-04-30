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

class PatchMealWithProducts(BaseModel):
  category: MealCategory | None = None
  name: str | None = None
  meal_products: list[MealProducts] | None = None

class MealResponse(BaseModel):
  category: MealCategory
  name: str
  user_id: int

class ProductInMeal(BaseModel):
  product_name: str
  grams: int

class MacroSummary(BaseModel):
  sum_of_kcal: float
  sum_of_protein: float
  sum_of_fat: float
  sum_of_carbs: float

class MealWithProductsResponse(BaseModel):
  category: MealCategory
  name: str
  user_id: int
  user_username: str
  products: list[ProductInMeal]
  macro: MacroSummary

class AllMealsByUserReponse(BaseModel):
  category: MealCategory
  name: str
  macro: MacroSummary