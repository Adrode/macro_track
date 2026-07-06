from pydantic import BaseModel
from datetime import datetime

class ResponseAI(BaseModel):
   context_session: int
   ai_response: str

class CreateMessageAI(BaseModel):
  context_session: int
  content: str