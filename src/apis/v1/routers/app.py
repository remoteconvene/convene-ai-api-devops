import structlog
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from src.core.config.settings import settings
from src.core.db.mongo_client_manager import mongo_client_manager
from src.core.db.sql_session_manager import engine

router = APIRouter(redirect_slashes=False)
logger = structlog.get_logger()


async def check_health():
    logger.info("Application health check initiated.")

    sql_healthy = True
    mongo_healthy = True

    if mongo_client_manager.is_connected() is not True:
        logger.error("MongoDB connection not found.")
        mongo_healthy = False

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except OperationalError:
        logger.error("MSSQL DB connection not found.")
        sql_healthy = False

    return {
        "status": "healthy" if mongo_healthy and sql_healthy else "unhealthy",
        "details": {"mongodb": mongo_healthy, "sql": sql_healthy},
    }


@router.get("/health/", response_model=dict)
async def health():
    response_data = await check_health()

    return JSONResponse(content=response_data)


@router.get("/version/", response_model=dict)
async def get_api_version():
    response_data = {"version": settings.CURRENT_API_VERSION}

    return JSONResponse(content=response_data)
