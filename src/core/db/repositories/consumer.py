from src.apis.v1.enums.status_type import StatusType
from src.apis.v1.models.consumer import ConsumerRegistrationRequest
from src.core.db.models.consumer import Consumer
from src.core.db.sql_session_manager import get_db


def add(consumer: ConsumerRegistrationRequest, consumer_id: str):
    with get_db() as db:
        consumer = Consumer(
            consumer_id=consumer_id,
            name=consumer.name,
            description=consumer.description,
            status=True,
        )
        db.add(consumer)
        db.commit()
        db.refresh(consumer)
        return consumer


def get_list():
    with get_db() as db:
        consumer_list = (
            db.query(Consumer).filter(Consumer.status == StatusType.ACTIVE.value).all()
        )
        return consumer_list


def get_consumer(consumer_id: str):
    with get_db() as db:
        consumer = (
            db.query(Consumer)
            .filter(
                Consumer.consumer_id == consumer_id,
            )
            .one_or_none()
        )
        return consumer
