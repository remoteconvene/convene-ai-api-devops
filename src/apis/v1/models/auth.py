from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class ConsumerAuthRequest(BaseModel):
    consumer_id: str
    jwt_token: str
    scopes: list[str]
    email: EmailStr
