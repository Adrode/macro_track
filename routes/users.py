from fastapi import APIRouter
from utils.dependencies import session_dependency

router = APIRouter()

@router.get("/me")
def me(db: session_dependency):
  pass