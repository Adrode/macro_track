from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = "users"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  email: Mapped[str] = mapped_column(unique=True)
  username: Mapped[Optional[str]]
  hashed_password: Mapped[str]
