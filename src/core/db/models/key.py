from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from src.core.db.base_class import Base


class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(500), nullable=False, unique=True)
