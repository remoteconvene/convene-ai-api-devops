from sqlalchemy.orm import Session

from src.core.db.models.key import Key
from src.core.db.sql_session_manager import get_db


def get_key():
    with get_db() as _db:
        db: Session = _db
        key = db.query(Key).filter(Key.id == 1).one()
        return key.title
