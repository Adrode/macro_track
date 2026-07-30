from fastapi import APIRouter
from models import models
from schemas import product_schemas
from utils.dependencies import session_dependency, current_trainer_dependency

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