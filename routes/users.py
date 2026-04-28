from fastapi import APIRouter
from sqlalchemy import select
from utils.dependencies import session_dependency
from utils.exceptions import not_found_exc
from schemas import user_schemas
from models import models

router = APIRouter()

@router.get("/{id}", response_model=user_schemas.ResponseUser)
def get_me(id: int, session: session_dependency):
  user = session.scalars(select(models.User).where(models.User.id == id)).first()

  if not user:
    raise not_found_exc

  return user

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