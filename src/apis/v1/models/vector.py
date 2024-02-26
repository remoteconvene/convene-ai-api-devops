from pydantic import BaseModel


class VectorRequest(BaseModel):
    id: int


class VectorResponse(BaseModel):
    result: int
