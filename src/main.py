import sys

# import threading

import structlog
from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from uvicorn import run

from src.apis.base import api_auth_router
from src.apis.base import api_router
from src.apis.v1.service.auth import get_user_or_consumer
from src.core.config.logging_setup import initialize_logging
from src.core.config.settings import settings
from src.core.db.base import Base
from src.core.db.mongo_client_manager import mongo_client_manager
from src.core.db.repositories.user import add_default_user
from src.core.db.sql_session_manager import engine

# from src.cron_job import configure_cron_job
# from src.cron_job import cron_job

logger = structlog.get_logger("main.py")


def init_fast_api():
    return FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


def connect_sql_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except OperationalError as e:
        print(f"Error connecting to the SQL DB: {e}")
        sys.exit()


def create_sql_tables():
    Base.metadata.create_all(bind=engine)


def create_default_sql_users():
    add_default_user()


def connect_mongo_db():
    connection_status = mongo_client_manager.initialize_client()

    if connection_status:
        print("Connected to MongoDB. Logging service is ready to initiate.")
        initialize_logging()
    else:
        print("Failed to connect to MongoDB. Logging service will not work.")
        sys.exit()


def include_router(api: FastAPI):
    api.include_router(api_auth_router)
    api.include_router(api_router, dependencies=[Depends(get_user_or_consumer)])


def configure_cors(api: FastAPI):
    origins = [
        "https://convene-ai-app.azurewebsites.net",
        "http://localhost:3000",
    ]
    api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# def setup_cron():
#     cron_thread = threading.Thread(target=cron_job)
#     cron_thread.start()
#     configure_cron_job()


def start_api():
    api = init_fast_api()
    connect_sql_db()
    create_sql_tables()
    create_default_sql_users()
    connect_mongo_db()
    include_router(api)
    configure_cors(api)
    # setup_cron()
    return api


app = start_api()


@app.get("/")
def root():
    return "Welcome to Convene AI API"


if __name__ == "__main__":
    run(app, host="convene-ai-app.azurewebsites.net")
