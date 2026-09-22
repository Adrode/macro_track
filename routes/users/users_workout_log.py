from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import models
from schemas import workout_log_schemas
from utils.dependencies import session_dependency, current_user_dependency
from utils.exceptions import not_authorized_token_exc

router = APIRouter()

@router.post("/", response_model=workout_log_schemas.WorkoutLogResponse)
def create_workout(
    data: workout_log_schemas.CreateWorkoutLog,
    session: session_dependency,
    current_user: current_user_dependency
):
    training_unit = session.scalars(select(models.TrainingUnit)
    .options(
        selectinload(models.TrainingUnit.training_exercises)
        .selectinload(models.TrainingExercise.exercise),

        selectinload(models.TrainingUnit.training_exercises)
        .selectinload(models.TrainingExercise.sets)
    )
    .where(
        models.TrainingPlan.id == data.training_plan_id,
        models.TrainingUnit.id == data.training_unit_id,
        models.TrainingPlan.user_id == current_user.id
    )
    ).first()

    if not training_unit:
        raise not_authorized_token_exc("Not authorized")

    new_workout_log = models.WorkoutLog(
        name = training_unit.name,
        start_time = data.date,
        user_id = current_user.id
    )
    session.add(new_workout_log)
    session.flush()

    for exercise in training_unit.training_exercises:
        new_workout_log_exercise = models.WorkoutLogExercise(
            exercise_name = exercise.exercise.name,
            workout_log_id = new_workout_log.id,
            exercise_order = exercise.exercise_order
        )
        session.add(new_workout_log_exercise)
        session.flush()
        for exercise_set in exercise.sets:
            new_workout_log_exercise_set = models.WorkoutLogExerciseSet(
                workout_log_exercise_id = new_workout_log_exercise.id,
                set_order = exercise_set.set_order,
                planned_repetitions = exercise_set.repetitions,
                performed_repetitions = 0
            )
            session.add(new_workout_log_exercise_set)

    session.commit()
    session.refresh(new_workout_log)

    response_exercises = []
    for exercise in new_workout_log.exercises:
        response_sets = []
        for exercise_set in exercise.sets:
            response_sets.append({
                "set_id": exercise_set.id,
                "planned_repetitions": exercise_set.planned_repetitions,
                "performed_repetitions": exercise_set.performed_repetitions
            })
        response_exercises.append({
            "exercise_id": exercise.id,
            "exercise_name": exercise.exercise_name,
            "sets": response_sets
        })

    response = {
        "id": new_workout_log.id,
        "name": new_workout_log.name,
        "start_time": new_workout_log.start_time,
        "exercises": response_exercises
    }

    return response