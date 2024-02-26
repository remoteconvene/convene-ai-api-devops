from src.core.db.models.log import Log
from src.core.db.sql_session_manager import get_db
from sqlalchemy.orm import Session


def add_log(log: str, type: str):
    with get_db() as _db:
        db: Session = _db
        log = Log(log=log, type=type)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
