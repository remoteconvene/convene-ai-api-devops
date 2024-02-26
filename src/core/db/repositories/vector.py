from datetime import datetime

from sqlalchemy.orm import Session

from src.apis.v1.enums.doc_type import DocType
from src.apis.v1.enums.status_type import StatusType
from src.core.config.settings import settings
from src.core.db.models.file import File
from src.core.db.sql_session_manager import get_db


def queue_status_repo(files_ids: list[str]):
    with get_db() as db:

        if len(files_ids) > 0:
            db_files = db.query(File).filter(File.id.in_(files_ids)).all()
        else:
            db_files = (
                db.query(File).filter(File.is_vectorized_completed is not True).all()
            )

        return db_files


def get_vectorization_files():
    with get_db() as db:

        db_files = (
            db.query(File)
            .filter(
                File.is_vectorized_completed == StatusType.DISABLED.value,
                File.file_type == DocType.DOC.value,
                File.file_ext.in_(settings.ALLOWED_FILE_TYPES_EXT),
                # File.last_vectorized_on == None,
            )
            .all()
        )

        return db_files


def update_vectorized_status(ids: list[int]):
    with get_db() as _db:
        db: Session = _db

        db.query(File).filter(File.id.in_(ids)).update(
            {
                File.is_vectorized_completed: True,
                File.last_vectorized_on: datetime.now(),
            },
            synchronize_session=False,
        )
        db.commit()
        db_files = db.query(File).filter(File.id.in_(ids)).all()

        return db_files


def update_file_status(id: int):
    with get_db() as _db:
        db: Session = _db

        db_file = (
            db.query(File)
            .filter(File.id == id)
            .update(
                {
                    File.is_vectorized_completed: True,
                    File.last_vectorized_on: datetime.now(),
                },
                synchronize_session=False,
            )
        )

        db.commit()

        return db_file
