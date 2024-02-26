from typing import List

from fastapi import APIRouter
from fastapi import Request
from fastapi import status

from src.apis.v1.models.thread import ChatHistoryRequest
from src.apis.v1.models.thread import ImageQueryRequest
from src.apis.v1.models.thread import QueryResponse
from src.apis.v1.models.thread import TextQueryRequest
from src.apis.v1.models.thread import ThreadResponse
from src.apis.v1.service.thread import close_thread_by_thread_id_ser
from src.apis.v1.service.thread import get_chat_history_ser
from src.apis.v1.service.thread import get_thread_by_thread_id_ser
from src.apis.v1.service.thread import get_threads_ser
from src.apis.v1.service.thread import image_query_ser
from src.apis.v1.service.thread import text_query_ser

router = APIRouter(redirect_slashes=False)


@router.get("/", response_model=List[ThreadResponse])
async def get_threads():
    return get_threads_ser()


@router.get("/{thread_id}", response_model=ThreadResponse)
async def get_thread_by_thread_id(thread_id: str):
    return get_thread_by_thread_id_ser(thread_id)


@router.patch("/{thread_id}/close/", status_code=status.HTTP_204_NO_CONTENT)
async def close_thread_by_thread_id(thread_id: str):
    close_thread_by_thread_id_ser(thread_id)


@router.post("/text-query/", response_model=QueryResponse)
async def text_query(
    text_query_req: TextQueryRequest,
    request: Request = None,
):
    return text_query_ser(text_query_req=text_query_req, request=request)


@router.post("/image-query/", response_model=QueryResponse)
async def image_query(
    image_query_req: ImageQueryRequest,
    request: Request = None,
):
    return image_query_ser(image_query_req=image_query_req, request=request)


@router.post("/chat-history/")
async def get_chat_history(chat_request: ChatHistoryRequest):
    return get_chat_history_ser(chat_request=chat_request)
