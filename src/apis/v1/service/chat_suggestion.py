from src.core.db.repositories.consumer import get_consumer
from src.core.langchain.openai import get_chat_suggestions_openai
from src.core.utils.validators import validate_uuid


def get_chat_suggestions_ser(consumer_id: str):
    validate_uuid(consumer_id)
    consumer = get_consumer(consumer_id)

    prompt = """List down 4 random questions from ESG topics having relations
    with 4 different documents in vector embeddings. Format per question
    with numbering and provide no other content with it."""

    # prompt = """List down 4 random questions related to Environmental, Social,
    # and Governance (ESG) topics that pertain to {consumer_name}.
    # These questions should be randomly selected and formatted with numbering.
    # Additionally, each question should have a relationship
    # with four distinct documents represented in vector embeddings """

    query = prompt.format(consumer_name=consumer.name)

    result = get_chat_suggestions_openai(query)
    return result
