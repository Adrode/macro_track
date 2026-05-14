from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from schemas import user_schemas
from models import models
from utils.dependencies import session_dependency
from utils.exceptions import not_found_exc, bad_request_exc
from authentication.pwd_hash import hash_password, verify_password
import authentication.short_tokens as auth
from schemas import auth_schemas

router = APIRouter()

@router.post("/register", response_model=user_schemas.ResponseUser)
def register(data: user_schemas.CreateUser, session: session_dependency):
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

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
  except IntegrityError:
    raise bad_request_exc
  
@router.post("/login")
def login(data: auth_schemas.LoginData, session: session_dependency):
  user = session.scalars(select(models.User).where(models.User.email == data.email)).first()

  if not user:
    raise not_found_exc
  if not verify_password(data.password, user.hashed_password):
    raise HTTPException(
      status_code=401,
      detail="Wrong email or password"
    )
  
  token = auth.create_access_token(
    data={"sub": data.email}
  )
  return {"access_token": token, "token_type": "bearer"}