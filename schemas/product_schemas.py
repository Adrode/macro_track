from pydantic import BaseModel, Field
from enum import Enum

class ProductCategory(str, Enum):
  protein="protein"
  fat="fat"
  carbs="carbs"
  fruits_vegetables="fruits/vegetables"

class CreateProduct(BaseModel):
  category: ProductCategory
  name: str
  kcal_per_100g: int = Field(ge=0)
  protein_per_100g: int = Field(ge=0)
  fat_per_100g: int = Field(ge=0)
  carbs_per_100g: int = Field(ge=0)

class ProductResponse(BaseModel):
  id: int
  category: ProductCategory
  name: str
  kcal_per_100g: int
  protein_per_100g: int
  fat_per_100g: int
  carbs_per_100g: int

class PatchProduct(BaseModel):
  category: ProductCategory | None = None
  name: str | None = None
  kcal_per_100g: int | None = Field(default=None, ge=0)
  protein_per_100g: int | None = Field(default=None, ge=0)
  fat_per_100g: int | None = Field(default=None, ge=0)
  carbs_per_100g: int  | None = Field(default=None, ge=0)