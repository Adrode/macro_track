from pydantic import BaseModel, Field

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

class TrainingPlanResponse(BaseModel):
    name: str