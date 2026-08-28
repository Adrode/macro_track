from fastapi import FastAPI
from routes.trainers import trainers_auth, trainers_connections, trainers, trainers_products, trainers_meals_for_users, trainers_exercises, trainers_training_plans_for_users
from routes.users import users_auth, users_ai, users_connections, users, users_diary, users_exercises, users_meals, users_products, users_training_plans

app = FastAPI()

app.include_router(users_auth.router, prefix="/auth/user", tags=["User: auth"])
app.include_router(trainers_auth.router, prefix="/auth/trainer", tags=["Trainer: auth"])
app.include_router(users_ai.router, prefix="/ai", tags=["User: AI"])
app.include_router(trainers.router, prefix="/trainer", tags=["Trainer: trainer"])
app.include_router(trainers_connections.router, prefix="/trainer/connections", tags=["Trainer: connections"])
app.include_router(trainers_products.router, prefix="/trainer/products", tags=["Trainer: products"])
app.include_router(trainers_exercises.router, prefix="/trainer/exercises", tags=["Trainer: exercises"])
app.include_router(trainers_meals_for_users.router, prefix="/trainer/meals", tags=["Trainer: meals for users"])
app.include_router(trainers_training_plans_for_users.router, prefix="/trainer/training_plans", tags=["Trainer: training plans for users"])
app.include_router(users.router, prefix="/user", tags=["User: user"])
app.include_router(users_connections.router, prefix="/user/connections", tags=["User: connections"])
app.include_router(users_products.router, prefix="/user/products", tags=["User: products"])
app.include_router(users_meals.router, prefix="/user/meals", tags=["User: meals"])
app.include_router(users_diary.router, prefix="/user/diary", tags=["User: diary"])
app.include_router(users_exercises.router, prefix="/user/exercises", tags=["User: exercises"])
app.include_router(users_training_plans.router, prefix="/user/training_plans", tags=["User: training plans"])