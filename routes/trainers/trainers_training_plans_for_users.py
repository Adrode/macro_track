from fastapi import APIRouter
from sqlalchemy import select
from models import models
from schemas import training_plans_schemas
from utils.dependencies import session_dependency, current_trainer_dependency
from utils.exceptions import not_authorized_token_exc

router = APIRouter()

@router.post("/{user_id}", response_model=training_plans_schemas.TrainingPlanResponse)
def create_training_plan_for_user(
    user_id: int,
    data: training_plans_schemas.CreateTrainingPlan,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    user = session.scalars(select(models.User).where(
        models.User.id == user_id
    )).first()

    if not user:
            raise not_authorized_token_exc("Not authorized")
    
    connection = session.scalars(select(models.TrainerUserConnection).where(
        models.TrainerUserConnection.status == "accepted",
        models.TrainerUserConnection.user_id == user.id,
        models.TrainerUserConnection.trainer_id == current_trainer.id
    )).first()

    if not connection or connection.status != "accepted":
        raise not_authorized_token_exc("No connection")

    new_training_plan_for_user = models.TrainingPlan(
        name = data.training_plan_name,
        description = data.training_plan_description,
        source = "trainer",
        user_id = user.id
    )

    session.add(new_training_plan_for_user)
    session.flush()

    exercise_ids = [
        exercise.exercise_id
        for unit in data.training_units
        for exercise in unit.training_exercises
    ]

    exercises = session.scalars(select(models.Exercise).where(
        models.Exercise.id.in_(exercise_ids)
    )).all()

    exercises_for_training_plan = []

    for exercise in exercises:
        if exercise.trainer_id == current_trainer.id and exercise.user_id is None:
            new_exercise_for_user = models.Exercise(
                name = exercise.name,
                main_muscles = exercise.main_muscles,
                side_muscles = exercise.side_muscles,
                description = exercise.description,
                user_id = user.id,
                trainer_id = None
            )
            session.add(new_exercise_for_user)
            session.flush()
            exercises_for_training_plan.append(new_exercise_for_user)
        elif exercise.trainer_id is None and exercise.user_id is None:
            exercises_for_training_plan.append(exercise)
        else:
            raise not_authorized_token_exc("Not authorized")

    for index1, item1 in enumerate(data.training_units):
        new_training_unit = models.TrainingUnit(
            training_plan = new_training_plan_for_user,
            name = item1.training_unit_name,
            description = item1.training_unit_description,
            unit_order = index1
        )
        session.add(new_training_unit)

        for index2, item2 in enumerate(item1.training_exercises):
            new_training_exercise = models.TrainingExercise(
                training_unit = new_training_unit,
                exercise_id = item2.exercise_id,
                exercise_order = index2
            )
            session.add(new_training_exercise)

            for index3, item3 in enumerate(item2.sets):
                new_training_exercise_set = models.TrainingExerciseSet(
                    training_exercise = new_training_exercise,
                    set_order = index3,
                    repetitions = item3.repetitions
                )
                session.add(new_training_exercise_set)

    session.commit()
    session.refresh(new_training_plan_for_user)

    response = {
        "training_plan_id": new_training_plan_for_user.id,
        "training_plan_name": new_training_plan_for_user.name,
        "training_plan_description": new_training_plan_for_user.description,
        "source": new_training_plan_for_user.source,
        "training_units": []
    }

    return response