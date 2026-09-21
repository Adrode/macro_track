from pydantic import BaseModel
from datetime import datetime

class CreateWorkoutLog(BaseModel):
    training_plan_id: int
    date: datetime