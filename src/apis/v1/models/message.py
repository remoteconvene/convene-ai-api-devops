from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from src.apis.v1.models.source import CreateSource
from src.apis.v1.models.source import SourceResponse


class CreateMessage(BaseModel):
    thread_id: Optional[int] = Field(default=None)
    file_id: Optional[int] = Field(default=None)
    query: str
    answer: str
    query_token_size: int
    answer_token_size: int
    ai_response_token_size: int
    query_type: str
    sources: List[CreateSource]


class MessageResponse(BaseModel):
    query: str
    answer: str
    created_on: datetime
    sources: List[SourceResponse]
