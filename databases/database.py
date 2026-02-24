from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings


# must remove connect_args when use other databases
engine = create_engine(settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10)

# This method for sqlite databases only⬇️
# engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


