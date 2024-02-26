from src.apis.v1.models.message import CreateMessage
from src.core.db.models.message import Message
from src.core.db.sql_session_manager import get_db


def add_new_message_to_thread(new_message: CreateMessage):
    with get_db() as db:
        message = Message.from_create_model(new_message)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
