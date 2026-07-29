from pydantic import BaseModel, EmailStr
from enum import Enum

class StatusType(str, Enum):
    pendind="pending"
    accepted="accepted"
    closed="closed"

class ManageStatusType(str, Enum):
    accepted="accepted"
    closed="closed"

class TrainerReponse(BaseModel):
    id: int
    email: EmailStr
    username: str

class ListConnectionStatusResponse(BaseModel):
    connection_id: int
    client_id: int
    client_username: str
    status: StatusType

class ListConnectionStatusWithTrainerResponse(BaseModel):
    connection_id: int
    trainer_id: int
    trainer_username: str
    status: StatusType

class ManageConnection(BaseModel):
    manage: ManageStatusType