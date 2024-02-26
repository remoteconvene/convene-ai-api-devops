from datetime import datetime
from typing import List

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from src.apis.v1.models.source import CreateSource
from src.core.db.base_class import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def from_create_model_list(
        cls, create_sources: List[CreateSource]
    ) -> "List[Source]":
        sources = []
        for create_source in create_sources:
            source = cls(title=create_source.title, url=create_source.url)
            sources.append(source)
        return sources
