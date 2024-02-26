from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from src.apis.v1.models.message import CreateMessage
from src.apis.v1.models.message import MessageResponse


class TextQueryRequest(BaseModel):
    query: str = Field(min_length=1)
    thread_id: Optional[str] = Field(max_length=128, default=None)


class CreateThread(BaseModel):
    thread_id: str
    external_user_id: int
    consumer_id: int | None = None
    messages: List[CreateMessage]


class SourceResponse(BaseModel):
    title: str
    url: str


class QueryResponse(BaseModel):
    thread_id: str
    response: str
    sources: List[SourceResponse]

    class ConfigDict:
        from_attributes = True


class ThreadResponse(BaseModel):
    thread_id: str
    consumer_id: int
    user_id: int
    status: bool
    created_on: datetime
    modified_on: datetime
    messages: List[MessageResponse]

    class ConfigDict:
        from_attributes = True


class ImageQueryRequest(BaseModel):
    file_id: int
    query: str = Field(min_length=1)
    thread_id: Optional[str] = Field(max_length=128, default=None)


class ChatHistoryRequest(BaseModel):
    thread_id: Optional[str] = Field(max_length=128, default=None)
    limit: int = 10
    chat_from: datetime | None = None
    chat_to: datetime | None = None
