from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from schemas import meal_schemas
from models import models
from utils.dependencies import session_dependency, current_trainer_dependency
from utils.exceptions import not_authorized_token_exc, bad_request_exc

router = APIRouter()

@router.post("/{user_id}") # , response_model=meal_schemas.MealResponse
def post_meal_for_user(
    user_id: int,
    data: meal_schemas.CreateMealWithProducts,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    try:
        user = session.scalars(select(models.User).where(models.User.id == user_id)).first()
        
        if not user:
            raise not_authorized_token_exc("Not authorized")

        trainers_products = []
        for item in data.meal_products:
            new_product = session.scalars(select(models.Product).where(
                models.Product.id == item.product_id
            )).first()

        new_meal_for_user = models.Meal(
            category=data.category,
            name=data.name,
            user_id=user.id,
            source="trainer"
        )

        session.add(new_meal_for_user)
        session.flush()

        new_user_products = []
        for item in trainers_products:
            new_product_for_user = models.Product(
                category=item.category,
                name=item.name,
                kcal_per_100g=item.kcal_per_100g,
                protein_per_100g=item.protein_per_100g,
                fat_per_100g=item.fat_per_100g,
                carbs_per_100g=item.carbs_per_100g,
                user_id=user.id
            )
            session.add(new_product_for_user)
            new_user_products.append(new_product_for_user)

        session.flush()

        for new_product, item in zip(new_user_products, data.meal_products):
            new_meal_product_for_user = models.MealProduct(
                meal_id=new_meal_for_user.id,
                product_id=new_product.id,
                grams=item.grams
            )
            session.add(new_meal_product_for_user)

        session.commit()
        session.refresh(new_meal_for_user)

        return new_meal_for_user

    except IntegrityError:
        raise bad_request_exc