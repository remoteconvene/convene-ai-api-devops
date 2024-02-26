import os

from dotenv import load_dotenv

current_path = os.getcwd()
env_path = f"{current_path}/.env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Convene AI API"
    PROJECT_VERSION: str = "1.0.0"
    CURRENT_API_VERSION: str = "v1"
    API_PREFIX = "/api/"

    # Microsoft SQL Server settings
    MSSQL_USER: str = os.getenv("MSSQL_USER")
    MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
    MSSQL_SERVER: str = os.getenv("MSSQL_SERVER")
    MSSQL_PORT: str = os.getenv("MSSQL_PORT")
    MSSQL_DB: str = os.getenv("MSSQL_DB")
    MSSQL_DRIVER: str = os.getenv("MSSQL_DRIVER", "ODBC+Driver+17+for+SQL+Server")
    DATABASE_URL = f"mssql+pyodbc://convene:Welcome123@convene-ai-sql-server.database.windows.net/convene_ai_db?driver=ODBC+Driver+17+for+SQL+Server"
    TEST_DATABASE_URL = f"mssql+pyodbc://convene:Welcome123@convene-ai-sql-server.database.windows.net/convene_ai_db?driver=ODBC+Driver+17+for+SQL+Server"

    # MongoDB Server settings
    MONGODB_HOST: str = os.getenv("MONGODB_HOST")
    MONGODB_PORT: str = os.getenv("MONGODB_PORT")
    MONGODB_USER: str = os.getenv("MONGODB_USER")
    MONGODB_PASSWORD: str = os.getenv("MONGODB_PASSWORD")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE")
    MONGODB_COLLECTION: str = os.getenv("MONGODB_COLLECTION")
    MONGODB_URL = (
        f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}"
    )
    MONGODB_CHAT_HISTORY_COLLECTION: str = os.getenv("MONGODB_CHAT_HISTORY_COLLECTION")

    # AWS Server settings
    AWS_SERVICE_NAME: str = os.getenv("AWS_SERVICE_NAME")
    AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_ACCESS_KEY_SECRET: str = os.getenv("AWS_ACCESS_KEY_SECRET")
    AWS_BUCKET_NAME: str = os.getenv("AWS_BUCKET_NAME")
    AWS_FOLDER_NAME: str = os.getenv("AWS_FOLDER_NAME")

    # JWT OPEN SSL Settings
    HEX32_OPENSSL_SECRET_KEY: str = os.getenv("HEX32_OPENSSL_SECRET_KEY")
    HEX32_OPENSSL_ALGORITHM: str = os.getenv("HEX32_OPENSSL_ALGORITHM")
    HEX32_OPENSSL_TOKEN_INFO: str = os.getenv("HEX32_OPENSSL_TOKEN_INFO")
    HEX32_OPENSSL_TOKEN_FORM: str = os.getenv("HEX32_OPENSSL_TOKEN_FORM")
    HEX32_OPENSSL_TOKEN_EXPIRY_MIN: str = os.getenv("HEX32_OPENSSL_TOKEN_EXPIRY_MIN")

    # Others
    FILE_UPLOAD_SIZE: int = int(os.getenv("FILE_UPLOAD_SIZE"))
    ALLOWED_FILE_TYPES: list[str] = ["application/pdf"]
    ALLOWED_FILE_TYPES_EXT: list[str] = [".pdf"]
    IMAGE_UPLOAD_SIZE: int = int(os.getenv("IMAGE_UPLOAD_SIZE"))
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/jpg", "image/png"]

    # OPEN AI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_VISION_MODEL: str = os.getenv("OPENAI_VISION_MODEL")
    OPENAI_VISION_API_URL: str = os.getenv("OPENAI_VISION_API_URL")
    OPENAI_VISION_MAX_TOKEN: int = int(os.getenv("OPENAI_VISION_MAX_TOKEN"))

    OPENAI_LLM_MODEL: str = os.getenv("OPENAI_LLM_MODEL")
    OPENAI_LLM_TEMP: int = int(os.getenv("OPENAI_LLM_TEMP"))
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL")
    TEXT_SPLIT_CHUNK_SIZE: int = int(os.getenv("TEXT_SPLIT_CHUNK_SIZE"))
    TEXT_SPLIT_CHUNK_OVERLAP: int = int(os.getenv("TEXT_SPLIT_CHUNK_OVERLAP"))
    VECTOR_DB_ESG_LOC: str = os.getenv("VECTOR_DB_ESG_LOC")
    VECTOR_DB_COLL_NAME: str = os.getenv("VECTOR_DB_COLL_NAME")

    # CRON JOB
    VECTORIZATION_CRON_TRIGGER_TIME: str = os.getenv("VECTORIZATION_CRON_TRIGGER_TIME")

    # ChROMA DB
    CHROMA_DB_HOST: str = os.getenv("CHROMA_DB_HOST")
    CHROMA_DB_PORT: int = int(os.getenv("CHROMA_DB_PORT"))


settings = Settings()
