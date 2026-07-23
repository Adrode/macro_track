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
  username: Mapped[str] = mapped_column(unique=True)
  hashed_password: Mapped[str]
  kcal_daily_goal: Mapped[int]
  protein_daily_goal: Mapped[int]
  fat_daily_goal: Mapped[int]
  carbs_daily_goal: Mapped[int]

  meals: Mapped[list["Meal"]] = relationship(back_populates="user", passive_deletes=True)
  products: Mapped[list["Product"]] = relationship(back_populates="user", passive_deletes=True)
  diary: Mapped[list["DiaryEntry"]] = relationship(back_populates="user", passive_deletes=True)
  ai_messages: Mapped[list["AIDetails"]] = relationship(back_populates="user", passive_deletes=True)
  trainer_connection: Mapped[list["TrainerClientConnection"]] = relationship(back_populates="client")

class Trainer(Base):
  __tablename__ = "trainers"

  id: Mapped[int] = mapped_column(primary_key=True)
  email: Mapped[str] = mapped_column(unique=True)
  username: Mapped[str] = mapped_column(unique=True)
  hashed_password: Mapped[str]

  client_connection: Mapped[list["TrainerClientConnection"]] = relationship(back_populates="trainer")
  products: Mapped[list["Product"]] = relationship(back_populates="trainer", passive_deletes=True)

class TrainerClientConnection(Base):
  __tablename__  = "trainer_client"

  id: Mapped[int] = mapped_column(primary_key=True)
  trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.id"))
  client_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  status: Mapped[str]
  created_at: Mapped[datetime]
  started_at: Mapped[datetime] = mapped_column(nullable=True)
  finished_at: Mapped[datetime] = mapped_column(nullable=True)

  trainer: Mapped[list["Trainer"]] = relationship(back_populates="client_connection")
  client: Mapped[list["User"]] = relationship(back_populates="trainer_connection")

class Product(Base):
  __tablename__ = "products"

  id: Mapped[int] = mapped_column(primary_key=True)
  category: Mapped[str]
  name: Mapped[str]
  kcal_per_100g: Mapped[int]
  protein_per_100g: Mapped[int]
  fat_per_100g: Mapped[int]
  carbs_per_100g: Mapped[int]
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
  trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.id", ondelete="CASCADE"), nullable=True)

  user: Mapped["User"] = relationship(back_populates="products")
  trainer: Mapped["Trainer"] = relationship(back_populates="products")

class Meal(Base):
  __tablename__ = "meals"

  id: Mapped[int] = mapped_column(primary_key=True)
  category: Mapped[str]
  name: Mapped[str]
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
  is_active: Mapped[bool] = mapped_column(default=True)

  user: Mapped["User"] = relationship(back_populates="meals")
  meal_products: Mapped[list["MealProduct"]] = relationship(passive_deletes=True)

class MealProduct(Base):
  __tablename__ = "meal_products"

  id: Mapped[int] = mapped_column(primary_key=True)
  meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id", ondelete="CASCADE"))
  product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
  grams: Mapped[int]

  product: Mapped["Product"] = relationship()

class DiaryEntry(Base):
  __tablename__ = "diaries_entry"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
  meal_category: Mapped[str]
  meal_name: Mapped[str] 
  meal_datetime: Mapped[datetime]

  user: Mapped["User"] = relationship(back_populates="diary")
  diary_meal_products: Mapped[list["DiaryMealProduct"]] = relationship(passive_deletes=True)

class DiaryMealProduct(Base):
  __tablename__ = "diaries_meal_products"

  id: Mapped[int] = mapped_column(primary_key=True)
  diary_id: Mapped[int] = mapped_column(ForeignKey("diaries_entry.id", ondelete="CASCADE"))
  name: Mapped[str]
  kcal_per_100g: Mapped[int]
  protein_per_100g: Mapped[int]
  fat_per_100g: Mapped[int]
  carbs_per_100g: Mapped[int]

class AIDetails(Base):
  __tablename__ = "ai_details"

  id: Mapped[int] = mapped_column(primary_key=True)
  context_session: Mapped[int]
  message: Mapped[str]
  message_role: Mapped[str]
  datetime: Mapped[datetime]
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

  user: Mapped["User"] = relationship(back_populates="ai_messages")


# TRZEBA ZROBIĆ USERS_DIARY NA ZASADZIE SNAPSHOTÓW, Z WŁASNYM DIARY_MEAL_PRODUCTS (też na snapshotach)
# MEAL I MEAL_PRODUCTS POZOSTAJĄ BEZ ZMIAN, PONIEWAŻ TO SĄ SZABLONY

# TEMPLATES mealsów dla trenera? jako snapshot samych nazw produktów z których składać ma się meals?

# TRENER MA WŁASNE PRODUKTY, a jak używa tego produktu dla meala który dodaje użytkownikowi, to dla tego usera w tabeli
# musi stworzyć się kopia tego produktu; najlepiej w formie trainer_id w products i tworzyć kopię; wtedy albo user_id albo trainer_id dla
# jednego wpisu musi być Null, bo ten sam rekord nie może mieć ownera trainer i user jednocześnie, ponieważ ma się to opierać na kopiach