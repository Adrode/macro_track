from fastapi import APIRouter
from sqlalchemy import select, and_, or_
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

    return new_training_plan