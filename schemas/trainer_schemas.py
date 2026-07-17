from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class TrainerReponse(BaseModel):
    id: int
    email: EmailStr
    username: str

class CreateConnection(BaseModel):
    trainer_id: int