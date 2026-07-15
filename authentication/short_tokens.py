import jwt, os
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import models
from utils.exceptions import not_authorized_token_exc
from database.database import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE_TIME = 30

def oauth2_scheme(role: str):
  return OAuth2PasswordBearer(
    tokenUrl=f"auth/{role}/login",
    scheme_name=f"OAuth2{role.capitalize()}"
  )

def create_access_token(data: dict, role: str):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_TIME)
  to_encode.update({"exp": expire, "role": role})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
  token: Annotated[str, Depends(oauth2_scheme("user"))],
  session: Annotated[Session, Depends(get_db)]
):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    role = payload.get("role")
    if not email or role != "user":
      raise not_authorized_token_exc("Not authorized")
      
  except InvalidTokenError:
    raise not_authorized_token_exc("Not authorized")
  
  user = session.scalars(select(models.User).where(models.User.email == email)).first()

  if not user:
    raise not_authorized_token_exc("Not authorized")
  
  return user

def get_current_trainer(
    token: Annotated[str, Depends(oauth2_scheme("trainer"))],
    session: Annotated[Session, Depends(get_db)]
):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    role = payload.get("role")
    if not email or role != "trainer":
      raise not_authorized_token_exc("Not authorized")
    
  except InvalidTokenError:
    raise not_authorized_token_exc("Not authorized")
  
  trainer = session.scalars(select(models.Trainer).where(models.Trainer.email == email)).first()

  if not trainer:
    raise not_authorized_token_exc("Not authorized")

  return trainer