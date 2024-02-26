from pydantic import BaseModel
from pydantic import Field


class ConsumerRegistrationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: str = Field(min_length=1, max_length=128)


class ConsumerRegistrationResponse(BaseModel):
    id: int
    consumer_id: str
    name: str
    description: str
    status: bool

    class ConfigDict:
        from_attributes = True
