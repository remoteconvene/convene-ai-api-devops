from pydantic import BaseModel


class ChatSuggestion(BaseModel):
    id: int
    consumer_id: int
    message: str
    type: str
    option: str
