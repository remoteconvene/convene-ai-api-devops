from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from src.core.db.base_class import Base


class Consumer(Base):
    __tablename__ = "consumers"

    id = Column(
        Integer, primary_key=True, autoincrement=True, index=True
    )  # Auto-generated ID
    consumer_id = Column(
        String(36), unique=True, nullable=False
    )  # Backend-generated UUID
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    status = Column(Boolean, default=True)  # Active or Inactive status
    created_on = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )  # Timestamp of creation
    modified_on = Column(
        DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )  # Timestamp of update
