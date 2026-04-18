from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

engine = create_engine('postgresql+psycopg2://macro_track_user:macro_track_passwd@localhost:5432/macro_track_db', echo=True)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()  