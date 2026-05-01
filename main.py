from fastapi import FastAPI
from routes import users, auth, products, meals, diary

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(meals.router, prefix="/meals", tags=["Meals"])
app.include_router(diary.router, prefix="/diary", tags=["Diary"])