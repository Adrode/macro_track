from pydantic import BaseModel
from datetime import datetime

class CreateWorkoutLog(BaseModel):
    training_plan_id: int
    training_unit_id: int
    date: datetime

class WorkoutLogExerciseSetsResponse(BaseModel):
    set_id: int
    planned_repetitions: int
    performed_repetitions: int

class WorkoutLogExercisesResponse(BaseModel):
    exercise_id: int
    exercise_name: str
    sets: list[WorkoutLogExerciseSetsResponse]

class WorkoutLogResponse(BaseModel):
    id: int
    name: str
    start_time: datetime
    exercises: list[WorkoutLogExercisesResponse]