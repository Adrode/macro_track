from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
  email: EmailStr
  username: str
  password: str
  kcal_daily_goal: int
  protein_daily_goal: int
  fat_daily_goal: int
  carbs_daily_goal: int

class ResponseUser(BaseModel):
  email: EmailStr
  username: str
  kcal_daily_goal: int
  protein_daily_goal: int
  fat_daily_goal: int
  carbs_daily_goal: int