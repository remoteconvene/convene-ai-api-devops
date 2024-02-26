from datetime import datetime
from typing import List

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.apis.v1.models.message import CreateMessage
from src.core.db.base_class import Base
from src.core.db.models.source import Source


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    thread_id = Column(Integer, ForeignKey("threads.id"), nullable=False)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=True)
    query = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    query_token_size = Column(Integer, nullable=False)
    answer_token_size = Column(Integer, nullable=False)
    ai_response_token_size = Column(Integer, nullable=False)
    query_type = Column(
        String(50), nullable=False
    )  # Query type based on API call ("text" or "image")
    created_on = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )  # Timestamp of creation

    sources = relationship(
        "Source", backref="message", cascade="all, delete-orphan", lazy="joined"
    )

    @classmethod
    def from_create_model_list(
        cls, create_messages: List[CreateMessage]
    ) -> "List[Message]":
        messages = []
        for create_message in create_messages:
            message = cls(
                thread_id=create_message.thread_id,
                file_id=create_message.file_id,
                query=create_message.query,
                answer=create_message.answer,
                query_token_size=create_message.query_token_size,
                answer_token_size=create_message.answer_token_size,
                ai_response_token_size=create_message.ai_response_token_size,
                query_type=create_message.query_type,
                sources=Source.from_create_model_list(create_message.sources),
            )
            messages.append(message)
        return messages

    @classmethod
    def from_create_model(cls, create_message: CreateMessage) -> "Message":
        return cls(
            thread_id=create_message.thread_id,
            file_id=create_message.file_id,
            query=create_message.query,
            answer=create_message.answer,
            query_token_size=create_message.query_token_size,
            answer_token_size=create_message.answer_token_size,
            ai_response_token_size=create_message.ai_response_token_size,
            query_type=create_message.query_type,
            sources=Source.from_create_model_list(create_message.sources),
        )
