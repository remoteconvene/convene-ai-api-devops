from typing import List

from src.apis.v1.models.thread import CreateThread
from src.core.db.models.thread import Thread
from src.core.db.sql_session_manager import get_db


def add_new_thread(new_thread: CreateThread):
    with get_db() as db:
        thread = Thread.from_create_model(new_thread)
        db.add(thread)
        db.commit()
        db.refresh(thread)
        return thread


def get_thread_by_thread_id(thread_id: str):
    with get_db() as db:
        thread: Thread = (
            db.query(Thread).filter(Thread.thread_id == thread_id).one_or_none()
        )
        return thread


def get_threads_repo():
    with get_db() as db:
        thread_list: List[Thread] = db.query(Thread).filter(Thread.status == 1).all()
        return thread_list


def close_thread_by_thread_id_repo(thread_id: str):
    with get_db() as db:
        db.query(Thread).filter(Thread.thread_id == thread_id).update({"status": False})
        db.commit()
