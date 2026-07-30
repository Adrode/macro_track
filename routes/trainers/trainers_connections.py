from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from sqlalchemy import select
from models import models
from schemas import trainer_schemas
from utils.dependencies import session_dependency, current_trainer_dependency
from utils.exceptions import not_authorized_token_exc

router = APIRouter()

@router.get("/", response_model=list[trainer_schemas.ListConnectionStatusResponse])
def list_connections(
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    connections = session.scalars(select(models.TrainerUserConnection).where(models.TrainerUserConnection.trainer_id == current_trainer.id)).all()

    response = []
    for item in connections:
        response.append({
            "connection_id": item.id,
            "user_id": item.user_id,
            "user_username": item.user.username,
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

@router.patch("/{conn_id}/manage")
def manage_invitation(
    conn_id: int,
    data: trainer_schemas.ManageConnection,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    connection = session.scalars(select(models.TrainerUserConnection).where(
        models.TrainerUserConnection.id == conn_id,
        models.TrainerUserConnection.trainer_id == current_trainer.id
    )).first()

    if not connection:
        raise not_authorized_token_exc("Not authorized")

    if data.manage == "closed":
        if connection.status == "closed":
            raise HTTPException(
                status_code=400,
                detail=f"Connection {connection.id} ID is already closed."
            )
        connection.status = "closed"
        connection.finished_at = datetime.now(timezone.utc)
    
    if data.manage == "accepted":
        if connection.status == "closed":
            raise HTTPException(
                status_code=400,
                detail=f"Connection {connection.id} ID is already closed. You can't reopen a closed connection."
            )
        if connection.status == "accepted":
            raise HTTPException(
                status_code=400,
                detail=f"Connection {connection.id} ID is already accepted."
            )
        connection.status = "accepted"
        connection.started_at = datetime.now(timezone.utc)

    session.commit()
    session.refresh(connection)
    
    return {"response": f"Connection with {connection.id} ID user {connection.status}"}