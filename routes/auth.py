from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from schemas import user_schemas, trainer_schemas
from models import models
from schemas import auth_schemas
from utils.dependencies import session_dependency
from utils.exceptions import not_found_exc, bad_request_exc, not_authorized_token_exc
from authentication.pwd_hash import hash_password, verify_password
import authentication.short_tokens as auth

router = APIRouter()

@router.post("/user/register", response_model=user_schemas.ResponseUser)
def user_register(data: auth_schemas.CreateUser, session: session_dependency):
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
  
@router.post("/user/login", response_model=auth_schemas.TokenResponse)
def user_login(
  session: session_dependency,
  data: OAuth2PasswordRequestForm = Depends()
):
  user = session.scalars(select(models.User).where(models.User.email == data.username)).first()

  if not user:
    raise not_authorized_token_exc("Wrong email or password")
  if not verify_password(data.password, user.hashed_password):
    raise not_authorized_token_exc("Wrong email or password")
  
  token = auth.create_access_token(
    data={
      "sub": user.email,
      "role": "user"
    }
  )
  return {"access_token": token, "token_type": "bearer"}

@router.post("/trainer/register", response_model=trainer_schemas.TrainerReponse)
def trainer_register(data: auth_schemas.CreateTrainer, session: session_dependency):
  try:
    new_trainer = models.Trainer(
      email=data.email,
      username=data.username,
      hashed_password=hash_password(data.password)
    )

    session.add(new_trainer)
    session.commit()
    session.refresh(new_trainer)

    return new_trainer
  except IntegrityError:
    raise bad_request_exc
  
@router.post("/trainer/login", response_model=auth_schemas.TokenResponse)
def trainer_login(
  session: session_dependency,
  data: OAuth2PasswordRequestForm = Depends()
):
  trainer = session.scalars(select(models.Trainer).where(models.Trainer.email == data.username)).first()

  if not trainer:
    raise not_authorized_token_exc("Wrong email or password")
  if not verify_password(data.password, trainer.hashed_password):
    raise not_authorized_token_exc("Wrong email or password")

  token = auth.create_access_token(
    data={
      "sub": trainer.email,
      "role": "trainer"
    }
  )

  return {"access_token": token, "token_type": "bearer"}