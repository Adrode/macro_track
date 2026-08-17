from fastapi import APIRouter
from sqlalchemy import select, or_, and_
from models import models
from schemas import exercise_schemas
from utils.dependencies import session_dependency, current_trainer_dependency
from utils.exceptions import not_authorized_token_exc

router = APIRouter()

@router.post("/", response_model=exercise_schemas.ExerciseResponse)
def create_exercise(
    data: exercise_schemas.CreateExercise,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    new_exercise = models.Exercise(
        name = data.name,
        main_muscles = data.main_muscles,
        side_muscles = data.side_muscles,
        description = data.description,
        trainer_id = current_trainer.id
    )

    session.add(new_exercise)
    session.commit()
    session.refresh(new_exercise)

    return new_exercise

@router.get("/{id}", response_model=exercise_schemas.ExerciseResponse)
def get_exercise(
    id: int,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    exercise = session.scalars(select(models.Exercise).where(
        models.Exercise.id == id,
        or_(
            models.Exercise.trainer_id == current_trainer.id,
            and_(
                models.Exercise.user_id == None,
                models.Exercise.trainer_id == None
            )
        )
    )).first()

    if not exercise:
        raise not_authorized_token_exc("Not authorized")

    return exercise

@router.get("/", response_model=list[exercise_schemas.ExerciseResponse])
def get_exercises(
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    exercises = session.scalars(select(models.Exercise).where(
        or_(
            models.Exercise.trainer_id == current_trainer.id,
            and_(
                models.Exercise.user_id == None,
                models.Exercise.trainer_id == None
            )
        )
    )).all()

    if not exercises:
        raise not_authorized_token_exc("Not authorized")

    return exercises

@router.delete("/{id}")
def delete_exercise(
    id: int,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    exercise = session.scalars(select(models.Exercise).where(
        models.Exercise.id == id,
        models.Exercise.trainer_id == current_trainer.id,
        models.Exercise.user_id == None
    )).first()

    if not exercise or exercise.trainer_id != current_trainer.id:
        raise not_authorized_token_exc("Not authorized")

    session.delete(exercise)
    session.commit()

    return {"detail": f"Exercise with ID {id} deleted"}

@router.patch("/{id}", response_model=exercise_schemas.ExerciseResponse)
def patch_exercise(
    id: int,
    data: exercise_schemas.PatchExercise,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    exercise = session.scalars(select(models.Exercise).where(
        models.Exercise.id == id,
        or_(
            models.Exercise.trainer_id == current_trainer.id,
            and_(
                models.Exercise.user_id == None,
                models.Exercise.trainer_id == None
            )
        )
    )).first()

    if not exercise:
        raise not_authorized_token_exc("Not authorized")

    to_patch = data.model_dump(exclude_unset=True)
    for key, value in to_patch.items():
        setattr(exercise, key, value)

    session.commit()
    session.refresh(exercise)

    return exercise