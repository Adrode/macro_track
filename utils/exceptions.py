from fastapi import HTTPException

not_found_exc = HTTPException(
  status_code=404,
  detail="Not found"
)