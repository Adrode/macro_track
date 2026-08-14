from pydantic import BaseModel, Field
from enum import Enum

class Muscles(str, Enum):
    chest = "chest"
    upper_chest = "upper_chest"
    lats = "lats"
    upper_back = "upper_back"
    lower_back = "lower_back"
    traps = "traps"
    front_delts = "front_delts"
    side_delts = "side_delts"
    rear_delts = "rear_delts"
    biceps = "biceps"
    triceps = "triceps"
    forearms = "forearms"
    abs = "abs"
    obliques = "obliques"
    quads = "quads"
    hamstrings = "hamstrings"
    glutes = "glutes"
    adductors = "adductors"
    calves = "calves"
    tibialis = "tibialis"

class TrainingPlanSource(str, Enum):
    user = "user"
    trainer = "trainer"

class CreateExercise(BaseModel):
    name: str
    main_muscles: list[Muscles]
    side_muscles: list[Muscles]
    description: str | None = None

class ExerciseResponse(BaseModel):
    id: int
    name: str
    main_muscles: list[Muscles]
    side_muscles: list[Muscles]
    description: str | None = None

class CreateTrainingPlan(BaseModel):
    name: str
    description: str | None
    source: TrainingPlanSource
