import base64
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from botocore.exceptions import ClientError
from fastapi import Request
from fastapi import status
from fastapi import UploadFile

from src.apis.v1.enums.doc_type import DocType
from src.apis.v1.enums.token_data import TokenData
from src.apis.v1.models.file import FileFilter
from src.apis.v1.service.consumer_token import get_token_detail
from src.core.config.settings import settings
from src.core.db.aws_client_manager import get_aws_client
from src.core.db.models.file import File
from src.core.db.repositories.file import add_file_repo
from src.core.db.repositories.file import get_files_repo
from src.core.utils.error_messages import errors
from src.core.utils.strings_constants import constants
from src.core.utils.throw_error import raise_error
from src.core.utils.token_size import get_token_from_header


def upload_file_ser(files: list[UploadFile], scopes: list[str], request: Request):
    bad_request = status.HTTP_400_BAD_REQUEST
    if len(files) == 0:
        raise_error(bad_request, errors.NO_FILES)

    if len(scopes) == 0:
        raise_error(bad_request, errors.NO_SCOPE_FOUND)

    for file in files:
        if file.content_type not in settings.ALLOWED_FILE_TYPES:
            raise_error(bad_request, errors.INVALID_FILE_TYPE)
        if file.size > int(settings.FILE_UPLOAD_SIZE):
            raise_error(
                bad_request,
                errors.LARGE_FILE,
            )

    s3_client = get_aws_client()
    token = get_token_from_header(request)
    data = get_token_detail(token)

    added_files = []
    for file in files:
        if not file_exists_in_aws(file, s3_client):
            aws_file_path = add_file_to_aws_bucket(file, s3_client)
            file = File(
                name=file.filename,
                consumer_id=data[TokenData.CONSUMER_ID],
                scopes=", ".join(scopes) if len(scopes) > 0 else None,
                file_path=aws_file_path,
                file_type=DocType.DOC.value,
                file_ext=Path(file.filename).suffix,
                file_size=file.size,
                status=True,
            )
            db_file = add_file_repo(file)
            added_files.append(db_file)

    return added_files


def upload_image_ser(image: UploadFile, request: Request):
    bad_request = status.HTTP_400_BAD_REQUEST
    if image is None:
        raise_error(bad_request, errors.NO_FILES)

    if image.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise_error(bad_request, errors.INVALID_IMAGE_TYPE)

    if image.size > int(settings.IMAGE_UPLOAD_SIZE):
        raise_error(
            bad_request,
            errors.LARGE_IMAGE,
        )

    suffix = Path(image.filename).suffix
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(image.file, tmp)
        image_path = Path(tmp.name)
        base64_image = encode_image(image_path)

        token = get_token_from_header(request)
        data = get_token_detail(token)

        file = File(
            name=image.filename,
            consumer_id=data[TokenData.CONSUMER_ID],
            scopes=data[TokenData.SCOPES],
            file_path=base64_image,
            file_type=DocType.IMAGE.value,
            file_ext=Path(image.filename).suffix,
            file_size=image.size,
            status=True,
        )

        db_file: File = add_file_repo(file)
        del db_file.file_path
        return db_file


def get_files_ser(filter: FileFilter):
    db_files = get_files_repo(filter=filter)

    s3_client = get_aws_client()
    aws_files = s3_client.list_objects_v2(Bucket=settings.AWS_BUCKET_NAME)
    result = {"db_files": db_files, "aws_files": aws_files}

    return result


def file_exists_in_aws(file: UploadFile, s3_client) -> bool:
    file_key = settings.AWS_FOLDER_NAME + "/" + file.filename

    result = s3_client.list_objects_v2(Bucket=settings.AWS_BUCKET_NAME, Prefix=file_key)
    if constants.CONTENTS in result:
        return True
    else:
        return False


def add_file_to_aws_bucket(file: UploadFile, s3_client):
    bucket_name = settings.AWS_BUCKET_NAME
    file_name = f"{settings.AWS_FOLDER_NAME}/{file.filename}"
    try:
        s3_client.upload_fileobj(
            file.file,
            bucket_name,
            file_name,
        )

        return f"https://{bucket_name}.s3.amazonaws.com/{file_name.replace(' ', '+')}"
    except ClientError as e:
        raise_error(status_code=status.HTTP_400_BAD_REQUEST, message=str(e.response))


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
