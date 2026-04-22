from fastapi import HTTPException

not_found_exc = HTTPException(
  status_code=404,
  detail="Not found"
)

bad_request_exc = HTTPException(
  status_code=400,
  detail="Bad request"
)