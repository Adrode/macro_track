from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from models import models
from schemas import trainer_schemas
from utils.dependencies import session_dependency, current_trainer_dependency, current_user_dependency
from utils.exceptions import not_authorized_token_exc, bad_request_exc
from datetime import datetime, timezone

router = APIRouter()

@router.get("/me", response_model=trainer_schemas.TrainerReponse)
def get_me(session: session_dependency, current_trainer: current_trainer_dependency):
    trainer = session.scalars(select(models.Trainer).where(models.Trainer.email == current_trainer.email)).first()

    if not trainer:
        raise not_authorized_token_exc("Not authorized")
    
    return trainer

@router.get("/all", response_model=list[trainer_schemas.TrainerReponse])
def get_all_trainers(session: session_dependency, get_current_user: current_user_dependency):
    trainers = session.scalars(select(models.Trainer)).all()

    if not trainers:
        raise not_authorized_token_exc("Not authorized")
    
    return trainers

@router.post("/invitation")
def send_invitation_to_trainer(
    data: trainer_schemas.CreateConnection,
    session: session_dependency,
    current_user: current_user_dependency
):
    try:
        trainer = session.scalars(select(models.Trainer).where(models.Trainer.id == data.trainer_id)).first()

        if not trainer:
            raise not_authorized_token_exc("Not authorized")

        new_connection = models.TrainerClientConnection(
            trainer_id=data.trainer_id,
            client_id=current_user.id,
            status="pending",
            created_at=datetime.now(timezone.utc)
        )

        session.add(new_connection)
        session.commit()
        session.refresh(new_connection)

        return True

    except IntegrityError:
        raise bad_request_exc