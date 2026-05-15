from fastapi import HTTPException

not_found_exc = HTTPException(
  status_code=404,
  detail="Not found"
)

bad_request_exc = HTTPException(
  status_code=400,
  detail="Bad request"
)

def not_authorized_token_exc(detail: str):
  return HTTPException(
    status_code=401,
    detail=detail,
    headers={"WWW-Authenticate": "Bearer"}
  )