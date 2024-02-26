from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from src.core.config.settings import settings
from src.core.db.repositories.key import get_key


def get_openai_embedding():
    key = get_key()
    embeddings = OpenAIEmbeddings(model=settings.OPENAI_EMBEDDING_MODEL, api_key=key)
    return embeddings


def get_chat_openai():
    key = get_key()
    llm = ChatOpenAI(
        model_name=settings.OPENAI_LLM_MODEL,
        temperature=settings.OPENAI_LLM_TEMP,
        api_key=key,
    )
    return llm
