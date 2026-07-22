from fastapi import APIRouter, HTTPException
from sqlalchemy import select, and_
from models import models
from schemas import trainer_schemas
from utils.dependencies import session_dependency, current_trainer_dependency, current_user_dependency
from utils.exceptions import not_authorized_token_exc
from datetime import datetime, timezone

router = APIRouter()

@router.get("/clients", response_model=list[trainer_schemas.ListConnectionStatusResponse])
def list_connections_with_clients(
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

@router.patch("/clients/manage")
def accept_invitation_from_client(
    data: trainer_schemas.ManageConnection,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    connection = session.scalars(select(models.TrainerClientConnection).where(
        and_(
            models.TrainerClientConnection.id == data.connection_id,
            models.TrainerClientConnection.trainer_id == current_trainer.id
        )
    )).first()

    if not connection:
        raise not_authorized_token_exc("Not authorized")

    if data.manage == "closed":
        if connection.status == "closed":
            raise HTTPException(
                status_code=400,
                detail=f"Connection {connection.id} ID is already closed"
            )
        connection.status = "closed"
    
    if data.manage == "accepted":
        if connection.status == "accepted":
            raise HTTPException(
                status_code=400,
                detail=f"Connection {connection.id} ID is already accepted"
            )
        connection.status = "accepted"
    
    connection.started_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(connection)
    
    return {"response": f"Connection with {connection.id} ID client {connection.status}"}

@router.post("/invitation")
def send_invitation_to_trainer(
    data: trainer_schemas.CreateConnection,
    session: session_dependency,
    current_user: current_user_dependency
):
    trainer = session.scalars(select(models.Trainer).where(models.Trainer.id == data.trainer_id)).first()
    valid_connection = session.scalars(select(models.TrainerClientConnection).where(
            and_(
                models.TrainerClientConnection.client_id == current_user.id,
                models.TrainerClientConnection.status != "closed"
            )
        )).all()

    if not trainer:
        raise not_authorized_token_exc("Not authorized")
    
    if valid_connection:
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

    return {"response": f"Invitation sent to {trainer.id} ID trainer"}

@router.get("/", response_model=list[trainer_schemas.ListConnectionStatusWithTrainerResponse])
def list_connections_with_trainers(
    session: session_dependency,
    current_user: current_user_dependency
):
    connections = session.scalars(select(models.TrainerClientConnection).where(models.TrainerClientConnection.client_id == current_user.id)).all()

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
    
@router.patch("/close")
def close_connection_with_trainer(
    data: trainer_schemas.ManageConnection,
    session: session_dependency,
    current_user: current_user_dependency
):
    connection = session.scalars(select(models.TrainerClientConnection).where(
        and_(
            models.TrainerClientConnection.id == data.connection_id,
            models.TrainerClientConnection.client_id == current_user.id
        )
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