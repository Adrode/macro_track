from fastapi import APIRouter
from sqlalchemy import select
from models import models
from schemas import trainer_schemas
from utils.dependencies import session_dependency, current_trainer_dependency, current_user_dependency
from utils.exceptions import not_authorized_token_exc

router = APIRouter()

@router.get("/me", response_model=trainer_schemas.TrainerReponse)
def get_me(session: session_dependency, current_trainer: current_trainer_dependency):
    trainer = session.scalars(select(models.Trainer).where(models.Trainer.email == current_trainer.email)).first()

    if not trainer:
        raise not_authorized_token_exc("Not authorized")
    
    return trainer

@router.get("/", response_model=list[trainer_schemas.TrainerReponse])
def get_all_trainers(session: session_dependency, get_current_user: current_user_dependency):
    trainers = session.scalars(select(models.Trainer)).all()

    if not trainers:
        raise not_authorized_token_exc("Not authorized")
    
    return trainers