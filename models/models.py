from datetime import datetime
from sqlalchemy import ForeignKey, CheckConstraint
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
  trainer_connection: Mapped[list["TrainerUserConnection"]] = relationship(back_populates="user")
  training_plans: Mapped[list["TrainingPlan"]] = relationship(back_populates="user", passive_deletes=True)

class Trainer(Base):
  __tablename__ = "trainers"

  id: Mapped[int] = mapped_column(primary_key=True)
  email: Mapped[str] = mapped_column(unique=True)
  username: Mapped[str] = mapped_column(unique=True)
  hashed_password: Mapped[str]

  user_connection: Mapped[list["TrainerUserConnection"]] = relationship(back_populates="trainer")
  products: Mapped[list["Product"]] = relationship(back_populates="trainer", passive_deletes=True)

class TrainerUserConnection(Base):
  __tablename__  = "trainer_user"

  id: Mapped[int] = mapped_column(primary_key=True)
  trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.id"))
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  status: Mapped[str]
  created_at: Mapped[datetime]
  started_at: Mapped[datetime] = mapped_column(nullable=True)
  finished_at: Mapped[datetime] = mapped_column(nullable=True)

  trainer: Mapped["Trainer"] = relationship(back_populates="user_connection")
  user: Mapped["User"] = relationship(back_populates="trainer_connection")

class Product(Base):
  __tablename__ = "products"
  __table_args__ = (
    CheckConstraint(
      "((user_id IS NULL) AND (trainer_id IS NOT NULL)) OR ((user_id IS NOT NULL) AND (trainer_id IS NULL)) OR ((user_id IS NULL) AND (trainer_id IS NULL))",
      name="product_owner_check",
    ),
  )

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
  source: Mapped[str]

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
  product_name: Mapped[str]
  kcal_per_100g: Mapped[int]
  protein_per_100g: Mapped[int]
  fat_per_100g: Mapped[int]
  carbs_per_100g: Mapped[int]
  grams: Mapped[int]

class AIDetails(Base):
  __tablename__ = "ai_details"

  id: Mapped[int] = mapped_column(primary_key=True)
  context_session: Mapped[int]
  message: Mapped[str]
  message_role: Mapped[str]
  datetime: Mapped[datetime]
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

  user: Mapped["User"] = relationship(back_populates="ai_messages")

class TrainingPlan(Base):
  __tablename__ = "training_plans"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  description: Mapped[str] = mapped_column(nullable=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

  user: Mapped["User"] = relationship(back_populates="training_plan")
  training_units: Mapped[list["TrainingUnit"]] = relationship(back_populates="training_plans", passive_deletes=True)

class TrainingUnit(Base):
  __tablename__ = "training_units"

  id: Mapped[int] = mapped_column(primary_key=True)
  training_plan_id: Mapped[int] = mapped_column(ForeignKey("training_plans.id", ondelete="CASCADE"))
  name: Mapped[str]
  description: Mapped[str] = mapped_column(nullable=True)

  training_plan: Mapped["TrainingPlan"] = relationship(back_populates="training_units")
  training_exercises: Mapped[list["TrainingExercise"]] = relationship(back_populates="training_unit", passive_deletes=True)

class TrainingExercise(Base):
  __tablename__ = "training_exercises"

  id: Mapped[int] = mapped_column(primary_key=True)
  training_unit_id: Mapped[int] = mapped_column(ForeignKey("training_units.id", ondelete="CASCADE"))
  exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id", ondelete="CASCADE"))
  exercise_order: Mapped[int]

  training_unit: Mapped["TrainingUnit"] = relationship(back_populates="training_exercises")
  sets: Mapped[list["TrainingExerciseSet"]] = relationship(back_populates="training_exercise", passive_deletes=True)

class TrainingExerciseSet(Base):
  __tablename__ = "training_exercises_sets"

  id: Mapped[int] = mapped_column(primary_key=True)
  training_exercise_id: Mapped[int] = mapped_column(ForeignKey("training_exercises.id", ondelete="CASCADE"))
  set_order: Mapped[int]
  repetitions: Mapped[int]

  training_exercise: Mapped["TrainingExercise"] = relationship(back_populates="sets")

class Exercise(Base):
  __tablename__ = "exercises"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  main_muscle: Mapped[str]
  side_muscle: Mapped[str] = mapped_column(nullable=True)
  description: Mapped[str] = mapped_column(nullable=True)

class WorkoutLog(Base):
  __tablename__ = "workout_logs"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  date: Mapped[datetime]
  duration: Mapped[int] = mapped_column(nullable=True)

  exercises: Mapped[list["WorkoutLogExercise"]] = relationship(back_populates="workout_log", passive_deletes=True)

class WorkoutLogExercise(Base):
  __tablename__ = "workout_log_exercises"

  id: Mapped[int] = mapped_column(primary_key=True)
  exercise_name: Mapped[str]
  workout_log_id: Mapped[int] = mapped_column(ForeignKey("workout_logs.id", ondelete="CASCADE"))
  exercise_order: Mapped[int]

  workout_log: Mapped["WorkoutLog"] = relationship(back_populates="exercises")
  sets: Mapped[list["WorkoutLogExerciseSet"]] = relationship(back_populates="exercise", passive_deletes=True)

class WorkoutLogExerciseSet(Base):
  __tablename__ = "workout_log_exercise_sets"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  workout_log_exercise_id: Mapped[int] = mapped_column(ForeignKey("workout_log_exercises.id", ondelete="CASCADE"))
  set_order: Mapped[int]
  repetitions: Mapped[int]
  weight: Mapped[int] = mapped_column(nullable=True)

  exercise: Mapped["WorkoutLogExercise"] = relationship(back_populates="sets")

  
  
# TEMPLATES mealsów dla trenera? jako snapshot samych nazw produktów z których składać ma się meals?