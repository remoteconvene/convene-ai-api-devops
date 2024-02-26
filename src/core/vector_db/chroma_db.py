# import chromadb
from langchain_community.vectorstores.chroma import Chroma

from src.core.config.settings import settings
from src.core.langchain.openai_config import get_openai_embedding

persist_directory = settings.VECTOR_DB_ESG_LOC + "/"


def get_vector_db_archived():
    vectordb = Chroma(
        collection_name=settings.VECTOR_DB_COLL_NAME,
        persist_directory=persist_directory,
        embedding_function=get_openai_embedding(),
    )
    return vectordb


def get_chroma_client_archived():
    # client = chromadb.PersistentClient(path=persist_directory)
    client = None
    return client


def get_chroma_client():
    # client = chromadb.HttpClient(
    #     host=settings.CHROMA_DB_HOST, port=settings.CHROMA_DB_PORT
    # )
    client = None
    return client


def get_vector_db():
    client = get_chroma_client()
    embedding = get_openai_embedding()

    vectordb = Chroma(
        client=client,
        collection_name=settings.VECTOR_DB_COLL_NAME,
        embedding_function=embedding,
    )
    return vectordb
