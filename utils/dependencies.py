from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models import models
from authentication.short_tokens import get_current_user

session_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[models.User, Depends(get_current_user)]