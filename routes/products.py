from fastapi import APIRouter
from sqlalchemy import select
from utils.dependencies import session_dependency
from utils.exceptions import not_found_exc
from models import models

router = APIRouter()

@router.get("/{id}")
def get_product(id: int, session: session_dependency):
  product = session.scalars(select(models.Product).where(models.Product.id == id)).first()

  if not product:
    raise not_found_exc
  
  return product