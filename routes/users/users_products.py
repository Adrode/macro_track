from fastapi import APIRouter
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from utils.dependencies import session_dependency, current_user_dependency
from utils.exceptions import not_found_exc, bad_request_exc, not_authorized_token_exc
from models import models
from schemas import product_schemas

router = APIRouter()

@router.post("/", response_model=product_schemas.ProductResponse)
def post_product(
  data: product_schemas.CreateProduct,
  session: session_dependency,
  current_user: current_user_dependency
):
  try:
    new_product = models.Product(
      category=data.category,
      name=data.name,
      kcal_per_100g=data.kcal_per_100g,
      protein_per_100g=data.protein_per_100g,
      fat_per_100g=data.fat_per_100g,
      carbs_per_100g=data.carbs_per_100g,
      user_id=current_user.id
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product
  except IntegrityError:
    raise bad_request_exc

@router.get("/{id}", response_model=product_schemas.ProductResponse)
def get_product(
  id: int,
  session: session_dependency,
  current_user: current_user_dependency
):
  product = session.scalars(select(models.Product).where(models.Product.id == id)).first()

  if not product:
    raise not_found_exc
  if product.user_id != None and product.user_id != current_user.id:
    raise not_authorized_token_exc("Not authorized")
  
  return product

@router.get("/", response_model=list[product_schemas.ProductResponse])
def get_products(
  session: session_dependency,
  current_user: current_user_dependency
):
  products = session.scalars(select(models.Product).where(
    or_(
      models.Product.user_id == None,
      models.Product.user_id == current_user.id
    )
  )).all()

  if not products:
    raise not_found_exc
  
  return products

@router.delete("/{id}")
def delete_product(
  id: int,
  session: session_dependency,
  current_user: current_user_dependency
):
  product = session.scalars(select(models.Product).where(models.Product.id == id)).first()

  if not product:
    raise not_found_exc
  
  if product.user_id == None or product.user_id != current_user.id:
    raise not_authorized_token_exc("Not authorized")

  session.delete(product)
  session.commit()
  return {"detail": f"Product with ID {product.id} deleted"}