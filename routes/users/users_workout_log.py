from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import models
from schemas import workout_log_schemas
from utils.dependencies import session_dependency, current_user_dependency
from utils.exceptions import not_authorized_token_exc
from datetime import datetime, timezone

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

@router.post("/", response_model=workout_log_schemas.WorkoutLogResponse)
def create_workout(
    data: workout_log_schemas.CreateWorkoutLog,
    session: session_dependency,
    current_user: current_user_dependency
):
    training_unit = session.scalars(select(models.TrainingUnit)
    .join(models.TrainingUnit.training_plan)
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
        start_time = datetime.now(timezone.utc),
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

    return workout_log_response(workout_log=new_workout_log)

@router.get("/{id}", response_model=workout_log_schemas.WorkoutLogResponse)
def get_workout_log(
    id: int,
    session: session_dependency,
    current_user: current_user_dependency
):
    workout_log = session.scalars(select(models.WorkoutLog)
    .options(
        selectinload(models.WorkoutLog.exercises)
        .selectinload(models.WorkoutLogExercise.sets)
    )
    .where(
        models.WorkoutLog.id == id,
        models.WorkoutLog.user_id == current_user.id
    )).first()

    if not workout_log:
        raise not_authorized_token_exc("Not authorized")

    return workout_log_response(workout_log=workout_log)

@router.get("/", response_model=list[workout_log_schemas.WorkoutLogsResponse])
def get_workout_logs(
    session: session_dependency,
    current_user: current_user_dependency
):
    workout_logs = session.scalars(select(models.WorkoutLog)
    .options(
        selectinload(models.WorkoutLog.exercises)
        .selectinload(models.WorkoutLogExercise.sets)
    )
    .where(
        models.WorkoutLog.user_id == current_user.id
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

@router.patch("/finish/{id}")
def finish_workout(
    id: int,
    session: session_dependency,
    current_user: current_user_dependency
):
    workout_log = session.scalars(select(models.WorkoutLog).where(
        models.WorkoutLog.id == id,
        models.WorkoutLog.user_id == current_user.id
    )).first()

    if not workout_log:
        raise not_authorized_token_exc("Not authorized")

    if workout_log.end_time is not None:
        raise not_authorized_token_exc("Workout is already finished")

    workout_log.end_time = datetime.now(timezone.utc)
    session.commit()
    session.refresh(workout_log)

    return {"detail": f"Workout ID {workout_log.id} finished at {workout_log.end_time}"}

@router.patch("/{workout_log_id}/exercise/{exercise_id}/set/{set_id}", response_model=workout_log_schemas.WorkoutLogResponse)
def add_repetitions(
    workout_log_id: int,
    exercise_id: int,
    set_id: int,
    data: workout_log_schemas.PatchRepetitions,
    session: session_dependency,
    current_user: current_user_dependency
):
    workout_set = session.scalars(select(models.WorkoutLogExerciseSet)
        .join(models.WorkoutLogExercise)
        .join(models.WorkoutLog)
        .where(
            models.WorkoutLog.id == workout_log_id,
            models.WorkoutLogExercise.id == exercise_id,
            models.WorkoutLogExercise.workout_log_id == workout_log_id,
            models.WorkoutLogExerciseSet.id == set_id,
            models.WorkoutLog.user_id == current_user.id
        )
    ).first()

    if not workout_set:
        raise not_authorized_token_exc("Not authorized")
    
    workout_log = session.scalars(select(models.WorkoutLog)
        .options(
            selectinload(models.WorkoutLog.exercises)
            .selectinload(models.WorkoutLogExercise.sets)
        )
        .where(
            models.WorkoutLog.id == workout_log_id,
            models.WorkoutLog.user_id == current_user.id
    )).first()

    if not workout_log:
        raise not_authorized_token_exc("Not authorized")

    if workout_log.end_time is not None:
        raise not_authorized_token_exc("Workout is already finished")

    workout_set.performed_repetitions = data.performed_repetitions

    session.commit()
    session.refresh(workout_log)

    return workout_log_response(workout_log=workout_log)