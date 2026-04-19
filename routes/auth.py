from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from schemas import schemas
from models import models
from utils.dependencies import session_dependency
from authentication.pwd_hash import hash_password

router = APIRouter()

@router.post("/register", response_model=schemas.ResponseUser)
def register(data: schemas.CreateUser, db: session_dependency):
  try:
    new_user = models.User(
      email=data.email,
      username=data.username,
      hashed_password=hash_password(data.password),
      kcal_daily_goal=data.kcal_daily_goal,
      protein_daily_goal=data.protein_daily_goal,
      fat_daily_goal=data.fat_daily_goal,
      carbs_daily_goal=data.carbs_daily_goal
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
  except IntegrityError:
    raise HTTPException(
      status_code=400,
      detail="Bad request"
    )