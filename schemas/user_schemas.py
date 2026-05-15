from pydantic import BaseModel, EmailStr

class PatchUser(BaseModel):
  email: EmailStr | None = None
  username: str | None = None
  kcal_daily_goal: int | None = None
  protein_daily_goal: int | None = None
  fat_daily_goal: int | None = None
  carbs_daily_goal: int | None = None

class ResponseUser(BaseModel):
  id: int
  email: EmailStr
  username: str
  kcal_daily_goal: int
  protein_daily_goal: int
  fat_daily_goal: int
  carbs_daily_goal: int