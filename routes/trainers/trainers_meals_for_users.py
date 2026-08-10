from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from schemas import meal_schemas
from models import models
from utils.dependencies import session_dependency, current_trainer_dependency
from utils.exceptions import not_authorized_token_exc, bad_request_exc

router = APIRouter()

@router.post("/{user_id}")
def post_meal_for_user(
    user_id: int,
    data: meal_schemas.CreateMealWithProducts,
    session: session_dependency,
    current_trainer: current_trainer_dependency
):
    try:
        user = session.scalars(select(models.User).where(models.User.id == user_id)).first()
        connection = session.scalars(select(models.TrainerUserConnection).where(
            models.TrainerUserConnection.status == "accepted",
            models.TrainerUserConnection.user_id == user.id,
            models.TrainerUserConnection.trainer_id == current_trainer.id
        )).first()

        if not user:
            raise not_authorized_token_exc("Not authorized")
        if not connection:
            raise not_authorized_token_exc("Not authorized")

        new_meal_for_user = models.Meal(
            category=data.category,
            name=data.name,
            user_id=user.id,
            source="trainer"
        )

        session.add(new_meal_for_user)
        session.flush()

        for item in data.meal_products:
            product = session.scalars(select(models.Product).where(
                models.Product.id == item.product_id
            )).first()

            if not product:
                raise not_authorized_token_exc("Not authorized")

            if product.trainer_id == current_trainer.id:
                new_product_for_user = models.Product(
                    category=product.category,
                    name=product.name,
                    kcal_per_100g=product.kcal_per_100g,
                    protein_per_100g=product.protein_per_100g,
                    fat_per_100g=product.fat_per_100g,
                    carbs_per_100g=product.carbs_per_100g,
                    user_id=user.id,
                    trainer_id=None
                )
                session.add(new_product_for_user)
                session.flush()
                product_id_for_meal = new_product_for_user.id
            elif product.trainer_id is None and product.user_id is None:
                product_id_for_meal = product.id
            else:
                raise not_authorized_token_exc("Not authorized")

            session.add(models.MealProduct(
                meal_id=new_meal_for_user.id,
                product_id=product_id_for_meal,
                grams=item.grams
            ))

        session.commit()
        session.refresh(new_meal_for_user)

        return new_meal_for_user

    except IntegrityError:
        raise bad_request_exc