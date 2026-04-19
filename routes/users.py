from fastapi import APIRouter
from sqlalchemy import select
from utils.dependencies import session_dependency
from schemas import schemas
from models import models

router = APIRouter()

@router.get("/{id}", response_model=schemas.ResponseUser)
def me(id: int, session: session_dependency):
  stmt = select(models.User).where(models.User.id == id)
  user = session.scalars(stmt).first()
  return user