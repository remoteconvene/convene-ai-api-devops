from fastapi import APIRouter
from fastapi import status

from src.apis.v1.service.chat_suggestion import get_chat_suggestions_ser

# from src.apis.v1.models.chat_suggestion import ChatSuggestion

router = APIRouter()


@router.get(
    "/{consumer_id}",
    status_code=status.HTTP_200_OK,
)
async def get_chat_suggestions(consumer_id: str):
    return get_chat_suggestions_ser(consumer_id)
