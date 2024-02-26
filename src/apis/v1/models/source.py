from datetime import datetime

from pydantic import BaseModel


class CreateSource(BaseModel):
    title: str
    url: str


class SourceResponse(BaseModel):
    title: str
    url: str
    created_on: datetime
