from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.apis.v1.models.thread import CreateThread
from src.core.db.base_class import Base
from src.core.db.models.message import Message


class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    thread_id = Column(String(36), nullable=False)
    external_user_id = Column(Integer, nullable=False)
    consumer_id = Column(Integer, ForeignKey("consumers.id"), nullable=True)
    status = Column(Boolean, default=True)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_on = Column(
        DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    messages = relationship(
        "Message", backref="thread", cascade="all, delete-orphan", lazy="joined"
    )

    @property
    def user_id(self):
        if self.external_user_id:
            return self.external_user_id
        else:
            return None

    @classmethod
    def from_create_model(cls, create_thread: CreateThread) -> "Thread":
        return cls(
            thread_id=create_thread.thread_id,
            external_user_id=create_thread.external_user_id,
            consumer_id=create_thread.consumer_id,
            messages=Message.from_create_model_list(create_thread.messages),
        )
