from fastapi import HTTPException

def not_found_exc(detail: str = "Not found"):
  return HTTPException(
    status_code=404,
    detail=detail
  )

def bad_request_exc(detail: str = "Bad request"):
  return HTTPException(
    status_code=400,
    detail=detail
  )

def not_authorized_token_exc(detail: str = "Unauthorized"):
  return HTTPException(
    status_code=401,
    detail=detail,
    headers={"WWW-Authenticate": "Bearer"}
  )