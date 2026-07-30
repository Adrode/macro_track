from fastapi import FastAPI
from routes import auth, products, meals, diary
from routes.trainers import trainers_connections, trainers
from routes.users import users_ai, users_connections, users

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users_ai.router, prefix="/ai", tags=["AI"])
app.include_router(trainers.router, prefix="/trainers", tags=["Trainers"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(trainers_connections.router, prefix="/trainer/connections", tags=["Trainers Connections"])
app.include_router(users_connections.router, prefix="/user/connections", tags=["Users Connections"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(meals.router, prefix="/meals", tags=["Meals"])
app.include_router(diary.router, prefix="/diary", tags=["Diary"])