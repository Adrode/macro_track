from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://macro_track_user:macro_track_passwd@localhost:5432/macro_track_db', echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  session = SessionLocal()
  try:
    yield session
  finally:
    session.close()