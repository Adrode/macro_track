from fastapi import APIRouter, HTTPException
from sqlalchemy import select, and_
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
        user = session.scalars(select(models.TrainerClientConnection).where(
                and_(
                    models.TrainerClientConnection.client_id == current_user.id,
                    models.TrainerClientConnection.status != "closed"
                )
            )).all()

        if not trainer:
            raise not_authorized_token_exc("Not authorized")
        
        if user:
            raise HTTPException(
                status_code=400,
                detail="This user already have a connection with a trainer."
            )

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

@router.get("/statuses", response_model=list[trainer_schemas.ListConnectionStatusResponse])
def list_connection_statuses(
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    connections = session.scalars(select(models.TrainerClientConnection).where(models.TrainerClientConnection.trainer_id == current_trainer.id)).all()

    response = []
    for item in connections:
        response.append({
            "connection_id": item.id,
            "client_id": item.client_id,
            "client_username": item.client.username,
            "status": item.status
        })

    order = {
        "pending": 0,
        "accepted": 1,
        "closed": 2
    }
    def order_key(item):
        return order[item['status']]

    response.sort(key=order_key)

    return response

@router.patch("/accept")
def accept_invitation_from_client(
    data: trainer_schemas.AcceptConnection,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    try:
        connection = session.scalars(select(models.TrainerClientConnection).where(
            and_(
                models.TrainerClientConnection.id == data.connection_id,
                models.TrainerClientConnection.trainer_id == current_trainer.id
            )
        )).first()

        if not connection:
            raise not_authorized_token_exc("Not authorized")

        connection.status = "accepted"
        session.commit()
        session.refresh(connection)
        
        return True
    except IntegrityError:
        raise bad_request_exc