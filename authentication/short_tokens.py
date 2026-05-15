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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_TIME)
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
  token: Annotated[str, Depends(oauth2_scheme)],
  session: Annotated[Session, Depends(get_db)]
):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    if not email:
      raise not_authorized_token_exc("Not authorized")
      
  except InvalidTokenError:
    raise not_authorized_token_exc("Not authorized")
  
  user = session.scalars(select(models.User).where(models.User.email == email)).first()

  if not user:
    raise not_authorized_token_exc("Not authorized")
  
  return user