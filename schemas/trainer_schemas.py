from pydantic import BaseModel, EmailStr
from enum import Enum

class StatusType(str, Enum):
    pendind="pending"
    accepted="accepted"
    closed="closed"

class TrainerReponse(BaseModel):
    id: int
    email: EmailStr
    username: str

class CreateConnection(BaseModel):
    trainer_id: int

class ListConnectionStatusResponse(BaseModel):
    connection_id: int
    client_id: int
    client_username: str
    status: StatusType

class AcceptConnection(BaseModel):
    connection_id: int