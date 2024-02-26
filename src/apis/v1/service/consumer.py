import uuid

from src.apis.v1.models.consumer import ConsumerRegistrationRequest
from src.core.db.repositories.consumer import add
from src.core.db.repositories.consumer import get_list


def register_new_consumer(consumer: ConsumerRegistrationRequest):
    consumer_id = str(uuid.uuid4())

    return add(consumer=consumer, consumer_id=consumer_id)


def get_consumers():
    return get_list()
