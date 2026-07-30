from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from models import models
from schemas import trainer_schemas
from utils.dependencies import session_dependency, current_user_dependency
from utils.exceptions import not_authorized_token_exc
from datetime import datetime, timezone

router = APIRouter()

@router.post("/{id}")
def send_invitation(
    id: int,
    session: session_dependency,
    current_user: current_user_dependency
):
    trainer = session.scalars(select(models.Trainer).where(models.Trainer.id == id)).first()
    valid_connection = session.scalars(select(models.TrainerUserConnection).where(
            models.TrainerUserConnection.user_id == current_user.id,
            models.TrainerUserConnection.status != "closed"
        )).all()

    if not trainer:
        raise not_authorized_token_exc("Not authorized")
    
    if valid_connection:
        raise HTTPException(
            status_code=400,
            detail="This user already have a connection with a trainer."
        )

    new_connection = models.TrainerUserConnection(
        trainer_id=id,
        user_id=current_user.id,
        status="pending",
        created_at=datetime.now(timezone.utc)
    )

    session.add(new_connection)
    session.commit()
    session.refresh(new_connection)

    return {"response": f"Invitation sent to {trainer.id} ID trainer"}

@router.get("/trainers", response_model=list[trainer_schemas.TrainerReponse])
def get_trainers(session: session_dependency, get_current_user: current_user_dependency):
    trainers = session.scalars(select(models.Trainer)).all()

    if not trainers:
        raise not_authorized_token_exc("Not authorized")
    
    return trainers

@router.get("/", response_model=list[trainer_schemas.ListConnectionStatusWithTrainerResponse])
def list_connections(
    session: session_dependency,
    current_user: current_user_dependency
):
    connections = session.scalars(select(models.TrainerUserConnection).where(models.TrainerUserConnection.user_id == current_user.id)).all()

    response = []
    for item in connections:
        response.append({
            "connection_id": item.id,
            "trainer_id": item.trainer_id,
            "trainer_username": item.trainer.username,
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
    
@router.patch("/{id}")
def close_connection(
    id: int,
    session: session_dependency,
    current_user: current_user_dependency
):
    connection = session.scalars(select(models.TrainerUserConnection).where(
        models.TrainerUserConnection.id == id,
        models.TrainerUserConnection.user_id == current_user.id
    )).first()

    if connection.status == "closed":
        raise HTTPException(
            status_code=400,
            detail=f"Connection {connection.id} ID is already closed"
        )
    
    if not connection:
        raise not_authorized_token_exc("Not authorized")
    
    connection.status = "closed"
    connection.finished_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(connection)

    return {"response": f"Connection {connection.id} ID closed"}