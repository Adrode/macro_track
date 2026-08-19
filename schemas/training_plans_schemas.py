from pydantic import BaseModel, Field
from typing import Literal

class CreateTrainingExerciseSets(BaseModel):
    repetitions: int = Field(gt=0)

class CreateTrainingExercises(BaseModel):
    exercise_id: int
    training_exercise_sets: list[CreateTrainingExerciseSets]

class CreateTrainingUnits(BaseModel):
    training_unit_name: str
    training_unit_description: str | None = None
    training_exercises: list[CreateTrainingExercises]

class CreateTrainingPlan(BaseModel):
    training_plan_name: str
    training_plan_description: str | None = None
    training_units: list[CreateTrainingUnits]

class ExerciseSets(BaseModel):
    repetitions: int

class TrainingExercise(BaseModel):
    exercise_name: str
    sets: list[ExerciseSets]

class TrainingUnitResponse(BaseModel):
    training_unit_name: str
    training_unit_description: str | None
    training_exercises: list[TrainingExercise]

class TrainingPlanResponse(BaseModel):
    training_plan_name: str
    training_plan_description: str | None
    source: Literal["user", "trainer"]
    training_units: list[TrainingUnitResponse]