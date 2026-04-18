from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = "users"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  email: Mapped[str] = mapped_column(unique=True)
  username: Mapped[Optional[str]]
  hashed_password: Mapped[str]
  kcal_daily_goal: Mapped[int]
  protein_daily_goal: Mapped[int]
  fat_daily_goal: Mapped[int]
  carbs_daily_goal: Mapped[int]

  meals: Mapped[list["Meal"]] = relationship()
  diary: Mapped[list["UserDiary"]] = relationship()

class Product(Base):
  __tablename__ = "products"

  id: Mapped[int] = mapped_column(primary_key=True)
  category: Mapped[str]
  name: Mapped[str]
  kcal_per_100g: Mapped[int]
  protein_per_100g: Mapped[int]
  fat_per_100g: Mapped[int]
  carbs_per_100g: Mapped[int]

class Meal(Base):
  __tablename__ = "meals"

  id: Mapped[int] = mapped_column(primary_key=True)
  category: Mapped[str]
  name: Mapped[str]
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

  meals_products: Mapped[list["MealProduct"]] = relationship()

class MealProduct(Base):
  __tablename__ = "meals_products"

  id: Mapped[int] = mapped_column(primary_key=True)
  meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"))
  product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
  grams: Mapped[int]

  product: Mapped["Product"] = relationship()

class UserDiary(Base):
  __tablename__ = "users_diary"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"))
  meal_datetime: Mapped[datetime]

  meal: Mapped["Meal"] = relationship()