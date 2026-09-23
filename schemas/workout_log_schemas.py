from pydantic import BaseModel, Field, field_serializer
from datetime import datetime, timedelta

class CreateWorkoutLog(BaseModel):
    training_plan_id: int
    training_unit_id: int

class WorkoutLogExerciseSetsResponse(BaseModel):
    workout_log_set_id: int
    planned_repetitions: int
    performed_repetitions: int

class WorkoutLogExercisesResponse(BaseModel):
    workout_log_exercise_id: int
    workout_log_exercise_name: str
    sets: list[WorkoutLogExerciseSetsResponse]

class WorkoutLogResponse(BaseModel):
    id: int
    name: str
    start_time: datetime
    end_time: datetime | None
    duration: timedelta | None
    exercises: list[WorkoutLogExercisesResponse]

    @field_serializer("duration")
    def serialize_duration(self, value: timedelta | None) -> float | None:
        if value is None:
            return None
        return value.total_seconds()

class WorkoutLogsResponse(BaseModel):
    id: int
    name: str
    start_time: datetime
    end_time: datetime | None

class FinishWorkout(BaseModel):
    end_time: datetime

class PatchRepetitions(BaseModel):
    performed_repetitions: int = Field(ge=0)