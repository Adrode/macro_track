from pydantic import BaseModel, EmailStr

class TrainerReponse(BaseModel):
    id: int
    email: EmailStr
    username: str