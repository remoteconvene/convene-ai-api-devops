from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from src.core.config.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
