import requests
from langchain.chains import RetrievalQA

from src.core.config.settings import settings
from src.core.langchain.openai_config import get_chat_openai
from src.core.vector_db.chroma_db import get_vector_db


def get_chat_suggestions_openai(query: str):
    vectordb = get_vector_db()
    llm = get_chat_openai()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, retriever=vectordb.as_retriever(), return_source_documents=True
    )

    result = qa_chain.invoke({"query": query})
    return result


def get_openai_vision_answer(image_base64: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
    }

    payload = {
        "model": settings.OPENAI_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64, {image_base64}"},
                    },
                ],
            }
        ],
        "max_tokens": int(settings.OPENAI_VISION_MAX_TOKEN),
    }

    response = requests.post(
        settings.OPENAI_VISION_API_URL, headers=headers, json=payload
    )
    data = response.json()
    answer = data["choices"][0]["message"]["content"]
    return answer
