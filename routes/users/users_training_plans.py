from fastapi import APIRouter
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from models import models
from schemas import training_plans_schemas
from utils.dependencies import session_dependency, current_user_dependency
from utils.exceptions import not_authorized_token_exc

router = APIRouter()

@router.post("/")
def create_training_plan(
    data: training_plans_schemas.CreateTrainingPlan,
    session: session_dependency,
    current_user: current_user_dependency
):    
    new_training_plan = models.TrainingPlan(
        name = data.training_plan_name,
        description = data.training_plan_description,
        user_id = current_user.id,
        source = "user"
    )
    session.add(new_training_plan)
    session.flush()

    for index1, item1 in enumerate(data.training_units):
        new_training_unit = models.TrainingUnit(
            training_plan_id = new_training_plan.id,
            name = item1.training_unit_name,
            description = item1.training_unit_description,
            unit_order = index1
        )
        session.add(new_training_unit)
        session.flush()

        for index2, item2 in enumerate(item1.training_exercises):
            exercise = session.scalars(select(models.Exercise).where(
                models.Exercise.id == item2.exercise_id,
                or_(
                    models.Exercise.user_id == current_user.id,
                    and_(
                        models.Exercise.user_id == None,
                        models.Exercise.trainer_id == None
                    )
                )
            )).first()

            if not exercise:
                raise not_authorized_token_exc("Not authorized")

            new_training_exercise = models.TrainingExercise(
                training_unit_id = new_training_unit.id,
                exercise_id = item2.exercise_id,
                exercise_order = index2
            )
            session.add(new_training_exercise)
            session.flush()

            for index3, item3 in enumerate(item2.training_exercise_sets):
                new_training_exercise_set = models.TrainingExerciseSet(
                    training_exercise_id = new_training_exercise.id,
                    set_order = index3,
                    repetitions = item3.repetitions
                )
                session.add(new_training_exercise_set)
                session.flush()

    session.commit()
    session.refresh(new_training_plan)

    return {"detail": f"Training plan {new_training_plan.name} created."}

@router.get("/{id}", response_model=training_plans_schemas.TrainingPlanResponse)
def get_training_plan(
    id: int,
    session: session_dependency,
    current_user: current_user_dependency
):
    training_plan = session.scalars(select(models.TrainingPlan)
        .options(
            selectinload(models.TrainingPlan.training_units)
            .selectinload(models.TrainingUnit.training_exercises)
            .selectinload(models.TrainingExercise.exercise),

            selectinload(models.TrainingPlan.training_units)
            .selectinload(models.TrainingUnit.training_exercises)
            .selectinload(models.TrainingExercise.sets)
        )
        .where(
            models.TrainingPlan.id == id,
            models.TrainingPlan.user_id == current_user.id
    )).first()

    if not training_plan:
        raise not_authorized_token_exc("Not authorized")

    training_units = []
    for unit in training_plan.training_units:
        training_exercises = []
        for exercise in unit.training_exercises:
            exercise_sets = []
            for exercise_set in exercise.sets:
                exercise_sets.append({
                    "repetitions": exercise_set.repetitions
                })
            training_exercises.append({
                "exercise_name": exercise.exercise.name,
                "sets": exercise_sets
            })
        training_units.append({
            "training_unit_name": unit.name,
            "training_unit_description": unit.description,
            "training_exercises": training_exercises
        })

    response = {
        "training_plan_name": training_plan.name,
        "training_plan_description": training_plan.description,
        "source": training_plan.source,
        "training_units": training_units
    }

    return response