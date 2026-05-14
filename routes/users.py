from fastapi import APIRouter, Depends
from sqlalchemy import select
from utils.dependencies import session_dependency
from utils.exceptions import not_found_exc
from schemas import user_schemas
from models import models
import authentication.short_tokens as auth

router = APIRouter()

@router.get("/", response_model=user_schemas.ResponseUser)
def get_me(
  current_user: models.User = Depends(auth.get_current_user)
):
  return current_user

@router.patch("/{id}", response_model=user_schemas.ResponseUser)
def patch_me(
    id: int,
    patch_data: user_schemas.PatchUser,
    session: session_dependency
):
  user = session.scalars(select(models.User).where(models.User.id == id)).first()

  if not user:
    raise not_found_exc

  patch = patch_data.model_dump(exclude_unset=True)
  for key, value in patch.items():
    setattr(user, key, value)
  session.commit()
  session.refresh(user)
  return user