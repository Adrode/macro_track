from fastapi import APIRouter
from sqlalchemy import select
from models import models
from schemas import workout_log_schemas
from utils.dependencies import session_dependency, current_user_dependency
from utils.exceptions import not_authorized_token_exc

router = APIRouter()

@router.post("/")
def create_workout(
    data: workout_log_schemas.CreateWorkoutLog,
    session: session_dependency,
    current_user: current_user_dependency
):
    training_plan = session.scalars(select(models.TrainingPlan).where(
        models.TrainingPlan.id == data.training_plan_id,
        models.TrainingPlan.user_id == current_user.id
    )).first()

    if not training_plan:
        raise not_authorized_token_exc("Not authorized")

    new_workout_log = models.WorkoutLog(
        name = training_plan.name,
        date = data.date,
    )

    session.add(new_workout_log)
    session.commit()
    session.refresh(new_workout_log)

    return {"detail": f"Workout log ID {new_workout_log.id} added"}