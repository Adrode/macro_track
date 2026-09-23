from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import models
from schemas import workout_log_schemas
from utils.dependencies import session_dependency, current_trainer_dependency
from utils.exceptions import not_authorized_token_exc

router = APIRouter()

def workout_log_response(workout_log):
    response_exercises = []
    for exercise in workout_log.exercises:
        response_sets = []
        for exercise_set in exercise.sets:
            response_sets.append({
                "workout_log_set_id": exercise_set.id,
                "planned_repetitions": exercise_set.planned_repetitions,
                "performed_repetitions": exercise_set.performed_repetitions
            })
        response_exercises.append({
            "workout_log_exercise_id": exercise.id,
            "workout_log_exercise_name": exercise.exercise_name,
            "sets": response_sets
        })

    if workout_log.end_time is not None:
        response = {
            "id": workout_log.id,
            "name": workout_log.name,
            "start_time": workout_log.start_time,
            "end_time": workout_log.end_time,
            "duration": workout_log.end_time - workout_log.start_time,
            "exercises": response_exercises
        }
    else:
        response = {
            "id": workout_log.id,
            "name": workout_log.name,
            "start_time": workout_log.start_time,
            "end_time": workout_log.end_time,
            "duration": None,
            "exercises": response_exercises
        }

    return response

@router.get("/user/{user_id}/log/{workout_log_id}", response_model=workout_log_schemas.WorkoutLogResponse)
def get_workout_log(
    user_id: int,
    workout_log_id: int,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    connection = session.scalars(select(models.TrainerUserConnection).where(
        models.TrainerUserConnection.status == "accepted",
        models.TrainerUserConnection.trainer_id == current_trainer.id,
        models.TrainerUserConnection.user_id == user_id
    )).first()

    if not connection:
            raise not_authorized_token_exc("Not authorized")
    
    workout_log = session.scalars(select(models.WorkoutLog)
    .options(
        selectinload(models.WorkoutLog.exercises)
        .selectinload(models.WorkoutLogExercise.sets)
    )
    .where(
        models.WorkoutLog.id == workout_log_id,
        models.WorkoutLog.user_id == user_id
    )).first()

    if not workout_log:
        raise not_authorized_token_exc("Not authorized")

    return workout_log_response(workout_log=workout_log)

@router.get("/user/{user_id}", response_model=list[workout_log_schemas.WorkoutLogsResponse])
def get_workout_logs_by_user(
    user_id: int,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    connection = session.scalars(select(models.TrainerUserConnection).where(
        models.TrainerUserConnection.status == "accepted",
        models.TrainerUserConnection.trainer_id == current_trainer.id,
        models.TrainerUserConnection.user_id == user_id
    )).first()

    if not connection:
        raise not_authorized_token_exc("Not authorized")
    
    workout_logs = session.scalars(select(models.WorkoutLog)
    .options(
        selectinload(models.WorkoutLog.exercises)
        .selectinload(models.WorkoutLogExercise.sets)
    )
    .where(
        models.WorkoutLog.user_id == user_id
    )).all()

    if not workout_logs:
        raise not_authorized_token_exc("Not authorized")

    response = [{
        "id": workout.id,
        "name": workout.name,
        "start_time": workout.start_time,
        "end_time": workout.end_time
    } for workout in workout_logs]

    return response