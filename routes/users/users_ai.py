import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from openai import OpenAI, OpenAIError
from fastapi import APIRouter, HTTPException
from sqlalchemy import select, and_
from schemas import ai_schemas
from utils.dependencies import current_user_dependency, session_dependency
from models import models

load_dotenv()

router = APIRouter()
client_ai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def messages_history(collection):
  return [
    {"role": element.message_role, "content": element.message} for element in collection 
  ]

@router.post("/chatbot", response_model=ai_schemas.ResponseAI)
def ask_ai(
  data: ai_schemas.CreateMessageAI,
  session: session_dependency,
  current_user: current_user_dependency
):
  try:
    new_user_details = models.AIDetails(
      context_session=data.context_session,
      message=data.content,
      message_role="user",
      datetime=datetime.now(timezone.utc),
      user_id=current_user.id
    )
    session.add(new_user_details)
    session.flush()

    history = session.scalars(select(models.AIDetails).where(
      and_(
        models.AIDetails.user_id == current_user.id,
        data.context_session == models.AIDetails.context_session
      )
    )).all()

    messages = messages_history(history)
    print(f"HISTORY: {messages}")

    response_ai = client_ai.responses.create(
      model="gpt-5-mini",
      instructions="You are a personal trainer that helps to compose a meal. If the user's question is not related to food/meals/diet, politely decline to answer." \
      "Return simple, concise answers. Return products in a list format. Suggest weights for products. Do not explain until asked.",
      input=messages
    )

    new_ai_details = models.AIDetails(
      context_session=data.context_session,
      message=response_ai.output_text,
      message_role="assistant",
      datetime=datetime.now(timezone.utc),
      user_id=current_user.id
    )
    session.add(new_ai_details)
    session.commit()

    response = {
      "context_session": data.context_session,
      "ai_response": response_ai.output_text
    }
    return response
  except OpenAIError:
    raise HTTPException(
      status_code=500,
      detail="AI Service Unavailable"
    )