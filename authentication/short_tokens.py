import jwt
from datetime import datetime, timezone, timedelta

SECRET_KEY = "dbfda6a759c6eb0e5fa5d05c8179e28093a5f0839cdc1a9bbe39198391ff8a81"
ALGORITHM = "HS256"
TOKEN_EXPIRE_TIME = 30

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_TIME)
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)