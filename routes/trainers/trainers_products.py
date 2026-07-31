from fastapi import APIRouter
from sqlalchemy import select, and_, or_
from models import models
from schemas import product_schemas
from utils.dependencies import session_dependency, current_trainer_dependency
from utils.exceptions import not_authorized_token_exc, bad_request_exc

router = APIRouter()

@router.post("/", response_model=product_schemas.ProductResponse)
def post_product(
    data: product_schemas.CreateProduct,
    session: session_dependency,
    currrent_trainer: current_trainer_dependency
):
    new_product = models.Product(
        category=data.category,
        name=data.name,
        kcal_per_100g=data.kcal_per_100g,
        protein_per_100g=data.protein_per_100g,
        fat_per_100g=data.fat_per_100g,
        carbs_per_100g=data.carbs_per_100g,
        trainer_id=currrent_trainer.id
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product

@router.get("/{id}", response_model=product_schemas.ProductResponse)
def get_product(
    id: int,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    product = session.scalars(select(models.Product).where(
        models.Product.id == id,
        models.Product.trainer_id == current_trainer.id
    )).first()

    if not product:
        raise not_authorized_token_exc("Not authorized")
    if product.user_id != None:
        raise bad_request_exc

    return product

@router.get("/", response_model=list[product_schemas.ProductResponse])
def get_products(
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    products = session.scalars(select(models.Product).where(
        or_(
            models.Product.trainer_id == current_trainer.id,
            and_(
                models.Product.user_id == None,
                models.Product.trainer_id == None
            )
        )
    )).all()

    if not products:
        raise not_authorized_token_exc("Not authorized")

    return products

@router.delete("/{id}")
def delete_product(
    id: int,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    product = session.scalars(select(models.Product).where(
        models.Product.id == id,
        models.Product.trainer_id == current_trainer.id
    )).first()

    if not product:
        raise not_authorized_token_exc("Not authorized")

    session.delete(product)
    session.commit()

    return {"detail": f"Product with ID {product.id} deleted"}