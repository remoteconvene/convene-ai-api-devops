from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from src.core.db.base_class import Base


class ConsumerToken(Base):
    __tablename__ = "consumer_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    consumer_id = Column(Integer, ForeignKey("consumers.id"), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    scopes = Column(String(255), nullable=False)
    jwt_token = Column(String, nullable=False)
    status = Column(Boolean, default=True)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_on = Column(
        DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )
