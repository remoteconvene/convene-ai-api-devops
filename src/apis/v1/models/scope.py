from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class ScopeRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: Optional[str] = Field(min_length=1, max_length=500)


class ScopeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: bool
    created_on: datetime
    modified_on: datetime = None


class ScopeRequestUpdate(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=128)
    description: Optional[str] = Field(min_length=1, max_length=500)
    status: Optional[bool]
