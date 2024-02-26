from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from src.core.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    superuser = Column(Boolean(), default=False)
    status = Column(Boolean(), default=True)
    jwt_token = Column(String, nullable=True)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_on = Column(
        DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
