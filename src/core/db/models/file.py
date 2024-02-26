from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from src.core.db.base_class import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    file_path = Column(String, nullable=False)
    consumer_id = Column(Integer, ForeignKey("consumers.id"), nullable=True)
    scopes = Column(String(255), nullable=True)
    file_type = Column(String(50), nullable=False)
    file_ext = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)
    is_vectorized_completed = Column(Boolean, default=False)
    last_vectorized_on = Column(DateTime, nullable=True, default=None)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_on = Column(
        DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )
