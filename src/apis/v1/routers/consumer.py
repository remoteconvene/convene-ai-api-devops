from typing import List

import structlog
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import status

from src.apis.dependencies import request_id_required
from src.apis.v1.models.consumer import ConsumerRegistrationRequest
from src.apis.v1.models.consumer import ConsumerRegistrationResponse
from src.apis.v1.service.consumer import get_consumers
from src.apis.v1.service.consumer import register_new_consumer

app = FastAPI()
router = APIRouter(redirect_slashes=False, dependencies=[Depends(request_id_required)])
logger = structlog.get_logger()


@router.post(
    "/",
    response_model=ConsumerRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_consumer(consumer: ConsumerRegistrationRequest):
    response_model = register_new_consumer(consumer=consumer)
    return response_model


@router.get("/", response_model=List[ConsumerRegistrationResponse])
async def get_consumer_list():
    response_model = get_consumers()
    return response_model
