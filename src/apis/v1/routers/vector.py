from fastapi import APIRouter
from fastapi import status

from src.apis.v1.service.vector import query_openai_llm_ser
from src.apis.v1.service.vector import query_vector_ser
from src.apis.v1.service.vector import queue_status_ser
from src.apis.v1.service.vector import vectorization_ser

router = APIRouter(redirect_slashes=False)


@router.get("/queue-status/", status_code=status.HTTP_200_OK)
def queue_status():
    return queue_status_ser()


@router.post("/")
def vectorization():
    return vectorization_ser()


@router.post("/query-vector/")
def query_vector(query: str):
    return query_vector_ser(query=query)


@router.post("/query-openai/")
def query_openai(query: str):
    return query_openai_llm_ser(query=query)
