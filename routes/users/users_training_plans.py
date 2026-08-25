from fastapi import APIRouter
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from models import models
from schemas import training_plans_schemas
from utils.dependencies import session_dependency, current_user_dependency
from utils.exceptions import not_authorized_token_exc

router = APIRouter()

@router.post("/", response_model=training_plans_schemas.TrainingPlanResponse)
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

    exercises_ids = {
        exercise.exercise_id for unit in data.training_units
        for exercise in unit.training_exercises
    }

    exercises = session.scalars(select(models.Exercise).where(
        models.Exercise.id.in_(exercises_ids),
        or_(
            models.Exercise.user_id == current_user.id,
            and_(
                models.Exercise.user_id == None,
                models.Exercise.trainer_id == None
            )
        )
    )).all()

    found_exercise_ids = {exercise.id for exercise in exercises}

    if not exercises_ids.issubset(found_exercise_ids):
        raise not_authorized_token_exc("Not authorized")

    for index1, item1 in enumerate(data.training_units):
        new_training_unit = models.TrainingUnit(
            training_plan = new_training_plan,
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

            for index3, item3 in enumerate(item2.training_exercise_sets):
                new_training_exercise_set = models.TrainingExerciseSet(
                    training_exercise = new_training_exercise,
                    set_order = index3,
                    repetitions = item3.repetitions
                )
                session.add(new_training_exercise_set)

    session.commit()
    session.refresh(new_training_plan)

    response = {
        "training_plan_id": new_training_plan.id,
        "training_plan_name": new_training_plan.name,
        "training_plan_description": new_training_plan.description,
        "source": new_training_plan.source,
        "training_units": []
    }

    return response

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
        "training_plan_id": training_plan.id,
        "training_plan_name": training_plan.name,
        "training_plan_description": training_plan.description,
        "source": training_plan.source,
        "training_units": training_units
    }

    return response

@router.get("/", response_model=list[training_plans_schemas.TrainingPlanResponse])
def get_training_plans(
    session: session_dependency,
    current_user: current_user_dependency
):
    training_plans = session.scalars(select(models.TrainingPlan)
        .options(
            selectinload(models.TrainingPlan.training_units)
        )
        .where(
            models.TrainingPlan.user_id == current_user.id
    )).all()

    if not training_plans:
        raise not_authorized_token_exc("Not authorized")

    response = []
    for training_plan in training_plans:
        response.append({
            "training_plan_id": training_plan.id,
            "training_plan_name": training_plan.name,
            "training_plan_description": training_plan.description,
            "source": training_plan.source,
            "training_units": [{
                "training_unit_name": training_unit.name,
                "training_unit_description": training_unit.description
            } for training_unit in training_plan.training_units]
        })

    return response

@router.delete("/{id}")
def delete_training_plan(
    id: int,
    session: session_dependency,
    current_user: current_user_dependency
):
    training_plan = session.scalars(select(models.TrainingPlan).where(
        models.TrainingPlan.id == id,
        models.TrainingPlan.user_id == current_user.id
    )).first()

    if not training_plan:
        raise not_authorized_token_exc("Not authorized")

    session.delete(training_plan)
    session.commit()

    return {"detail": f"Training plan ID {training_plan.id} removed."}

@router.put("/{id}", response_model=training_plans_schemas.TrainingPlanResponse)
def update_training_plan(
    id: int,
    data: training_plans_schemas.UpdateTrainingPlan,
    session: session_dependency,
    current_user: current_user_dependency
):
    training_plan = session.scalars(select(models.TrainingPlan).where(
        models.TrainingPlan.id == id,
        models.TrainingPlan.user_id == current_user.id
    )).first()

    if not training_plan:
        raise not_authorized_token_exc("Not authorized")

    training_plan.name = data.training_plan_name
    training_plan.description = data.training_plan_description

    for unit in training_plan.training_units:
        session.delete(unit)
    session.flush()

    exercises_ids = {
        exercise.exercise_id for unit in data.training_units
        for exercise in unit.training_exercises
    }

    exercises = session.scalars(select(models.Exercise).where(
        models.Exercise.id.in_(exercises_ids),
        or_(
            models.Exercise.user_id == current_user.id,
            and_(
                models.Exercise.user_id == None,
                models.Exercise.trainer_id == None
            )
        )
    )).all()

    found_exercise_ids = {exercise.id for exercise in exercises}

    if not exercises_ids.issubset(found_exercise_ids):
        raise not_authorized_token_exc("Not authorized")

    for index1, item1 in enumerate(data.training_units):
        new_training_unit = models.TrainingUnit(
            training_plan = training_plan,
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

            for index3, item3 in enumerate(item2.training_exercise_sets):
                new_training_exercise_set = models.TrainingExerciseSet(
                    training_exercise = new_training_exercise,
                    set_order = index3,
                    repetitions = item3.repetitions
                )
                session.add(new_training_exercise_set)

    session.commit()
    session.refresh(training_plan)

    response = {
        "training_plan_id": training_plan.id,
        "training_plan_name": training_plan.name,
        "training_plan_description": training_plan.description,
        "source": training_plan.source,
        "training_units": []
    }

    return response