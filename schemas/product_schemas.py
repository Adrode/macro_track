from pydantic import BaseModel
from enum import Enum

class ProductCategory(str, Enum):
  protein="protein"
  fat="fat"
  carbs="carbs"
  fruits_vegetables="fruits_vegetables"

class CreateProduct(BaseModel):
  category: ProductCategory
  name: str
  kcal_per_100g: int
  protein_per_100g: int
  fat_per_100g: int
  carbs_per_100g: int
  user_id: int