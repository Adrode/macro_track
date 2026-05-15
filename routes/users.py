from fastapi import APIRouter
from sqlalchemy import select
from utils.dependencies import session_dependency, current_user_dependency
from utils.exceptions import not_found_exc
from schemas import user_schemas
from models import models
import authentication.short_tokens as auth

router = APIRouter()

@router.get("/", response_model=user_schemas.ResponseUser)
def get_me(
  current_user: current_user_dependency
):
  return current_user

@router.patch("/", response_model=user_schemas.ResponseUser)
def patch_me(
    patch_data: user_schemas.PatchUser,
    session: session_dependency,
    current_user: current_user_dependency
):
  user = session.scalars(select(models.User).where(models.User.id == current_user.id)).first()

  if not user:
    raise not_found_exc

  patch = patch_data.model_dump(exclude_unset=True)
  for key, value in patch.items():
    setattr(user, key, value)
  session.commit()
  session.refresh(user)
  return user