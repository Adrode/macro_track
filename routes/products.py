from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from utils.dependencies import session_dependency
from utils.exceptions import not_found_exc, bad_request_exc
from models import models
from schemas import product_schemas

router = APIRouter()

@router.post("/")
def post_product(data: product_schemas.CreateProduct, session: session_dependency):
  try:
    new_product = models.Product(
      category=data.category,
      name=data.name,
      kcal_per_100g=data.kcal_per_100g,
      protein_per_100g=data.protein_per_100g,
      fat_per_100g=data.fat_per_100g,
      carbs_per_100g=data.carbs_per_100g,
      user_id=data.user_id
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product
  except IntegrityError:
    raise bad_request_exc

@router.get("/{id}")
def get_product(id: int, session: session_dependency):
  product = session.scalars(select(models.Product).where(models.Product.id == id)).first()

  if not product:
    raise not_found_exc
  
  return product

@router.get("/")
def get_products(session: session_dependency):
  products = session.scalars(select(models.Product)).all()

  if not products:
    raise not_found_exc
  
  return products