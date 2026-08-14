from fastapi import APIRouter
from models import models
from schemas import training_schemas
from utils.dependencies import session_dependency, current_user_dependency

router = APIRouter()

@router.post("/exercise", response_model=training_schemas.ExerciseResponse)
def create_exercise(
    data: training_schemas.CreateExercise,
    session: session_dependency,
    current_user: current_user_dependency
):
    new_exercise = models.Exercise(
        name = data.name,
        main_muscles = data.main_muscles,
        side_muscles = data.side_muscles,
        description = data.description,
        user_id = current_user.id
    )

    session.add(new_exercise)
    session.commit()
    session.refresh(new_exercise)

    return new_exercise

@router.post("/")
def create_training_plan():
    pass