from fastapi import APIRouter
from fastapi import Depends

from src.apis.dependencies import request_id_required
from src.apis.v1.routers import app
from src.apis.v1.routers import auth
from src.apis.v1.routers import chat_suggestion
from src.apis.v1.routers import consumer
from src.apis.v1.routers import file
from src.apis.v1.routers import scope
from src.apis.v1.routers import thread
from src.apis.v1.routers import vector
from src.core.config.settings import settings

api_router = APIRouter(dependencies=[Depends(request_id_required)])
api_router.include_router(
    app.router,
    prefix=settings.API_PREFIX + settings.CURRENT_API_VERSION + "/app",
    tags=["app"],
)
api_router.include_router(
    scope.router,
    prefix=settings.API_PREFIX + settings.CURRENT_API_VERSION + "/scopes",
    tags=["scopes"],
)
api_router.include_router(
    file.router,
    prefix=settings.API_PREFIX + settings.CURRENT_API_VERSION + "/files",
    tags=["files"],
)
api_router.include_router(
    thread.router,
    prefix=settings.API_PREFIX + settings.CURRENT_API_VERSION + "/threads",
    tags=["threads"],
)
api_router.include_router(
    chat_suggestion.router,
    prefix=settings.API_PREFIX + settings.CURRENT_API_VERSION + "/chat",
    tags=["chat"],
)


api_auth_router = APIRouter()
api_auth_router.include_router(
    auth.router,
    prefix=settings.API_PREFIX + settings.CURRENT_API_VERSION + "/auth",
    tags=["auth"],
)
api_auth_router.include_router(
    consumer.router,
    prefix=settings.API_PREFIX + settings.CURRENT_API_VERSION + "/consumers",
    tags=["consumers"],
)
api_auth_router.include_router(
    vector.router,
    prefix=settings.API_PREFIX + settings.CURRENT_API_VERSION + "/vectorization",
    tags=["vectorization"],
)
