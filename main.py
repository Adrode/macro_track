from fastapi import FastAPI
from routes import auth
from routes.trainers import trainers_connections, trainers
from routes.users import users_ai, users_connections, users, users_diary, users_meals, users_products

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users_ai.router, prefix="/ai", tags=["Users AI"])
app.include_router(trainers.router, prefix="/trainer", tags=["Trainers"])
app.include_router(users.router, prefix="/user", tags=["Users"])
app.include_router(trainers_connections.router, prefix="/trainer/connections", tags=["Trainers connections"])
app.include_router(users_connections.router, prefix="/user/connections", tags=["Users connections"])
app.include_router(users_products.router, prefix="/user/products", tags=["Users products"])
app.include_router(users_meals.router, prefix="/user/meals", tags=["Users meals"])
app.include_router(users_diary.router, prefix="/user/diary", tags=["Users diary"])