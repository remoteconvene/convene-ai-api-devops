from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from src.core.db.base_class import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    log = Column(String, nullable=False, unique=True)
    type = Column(String(50), nullable=False, unique=True)
