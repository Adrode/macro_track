from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.database import get_db

app = FastAPI()

@app.get('/kekw')
def kekw(db: Session = Depends(get_db)):
  pass