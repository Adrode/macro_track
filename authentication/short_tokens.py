import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy import select
from models import models
from utils.dependencies import session_dependency
from utils.exceptions import not_found_exc

SECRET_KEY = "dbfda6a759c6eb0e5fa5d05c8179e28093a5f0839cdc1a9bbe39198391ff8a81"
ALGORITHM = "HS256"
TOKEN_EXPIRE_TIME = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_TIME)
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
  token: Annotated[str, Depends(oauth2_scheme)],
  session: session_dependency
):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    if not email:
      raise HTTPException(
        status_code=401,
        detail="Not authorized"
      )
  except InvalidTokenError:
    raise HTTPException(
        status_code=401,
        detail="Not authorized"
      )
  
  user = session.scalars(select(models.User).where(models.User.email == email)).first()

  if not user:
    raise not_found_exc
  
  return user