from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from src.core.db.base_class import Base


class Scope(Base):
    __tablename__ = "scopes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Boolean(), default=True)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_on = Column(
        DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )
