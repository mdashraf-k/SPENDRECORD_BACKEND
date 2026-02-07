from databases.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(250), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


