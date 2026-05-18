from enum import Enum
from pydantic import BaseModel, Field

class MealCategory(str, Enum):
  breakfast = "breakfast"
  brunch = "brunch"
  lunch = "lunch"
  dinner = "dinner"
  supper = "supper"

class MealProducts(BaseModel):
  product_id: int
  grams: int = Field(gt=0)

class CreateMealWithProducts(BaseModel):
  category: MealCategory
  name: str
  meal_products: list[MealProducts]

class PatchMealWithProducts(BaseModel):
  category: MealCategory | None = None
  name: str | None = None
  meal_products: list[MealProducts] | None = None

class PatchMealIsActive(BaseModel):
  is_active: bool

class MealIsActiveResponse(BaseModel):
  id: int
  name: str
  is_active: bool

class MealResponse(BaseModel):
  id: int
  category: MealCategory
  name: str

class ProductInMeal(BaseModel):
  product_id: int
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
  is_active: bool
  products: list[ProductInMeal]
  macro: MacroSummary

class AllMealsByUserReponse(BaseModel):
  id: int
  category: MealCategory
  name: str
  is_active: bool
  macro: MacroSummary