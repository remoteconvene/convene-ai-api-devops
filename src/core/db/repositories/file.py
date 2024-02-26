from fastapi import HTTPException
from fastapi import status

from src.apis.v1.enums.doc_type import DocType
from src.apis.v1.models.file import FileFilter
from src.core.db.models.file import File
from src.core.db.sql_session_manager import get_db
from src.core.utils.error_messages import errors


def add_file_repo(file: File):
    with get_db() as db:
        db.add(file)
        db.commit()
        db.refresh(file)
        return file


def get_files_repo(filter: FileFilter):
    with get_db() as db:
        db_files = db.query(File).filter(File.file_type == DocType.DOC.value).all()
    return db_files


def get_image_base64(id: int):
    with get_db() as db:
        file = db.query(File).filter(File.id == id).one_or_none()
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=errors.INVALID_FILE_ID
            )
        return file.file_path
