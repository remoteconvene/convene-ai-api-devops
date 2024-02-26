from fastapi import APIRouter
from fastapi import File
from fastapi import Form
from fastapi import Request
from fastapi import status
from fastapi import UploadFile
from typing_extensions import Annotated

from src.apis.v1.models.file import FileFilter
from src.apis.v1.service.file import get_files_ser
from src.apis.v1.service.file import upload_file_ser
from src.apis.v1.service.file import upload_image_ser
from src.core.utils.strings_constants import constants

router = APIRouter(redirect_slashes=False)


@router.post("/upload-files/", status_code=status.HTTP_201_CREATED)
def upload_files(
    files: Annotated[list[UploadFile], File(description=constants.UPLOAD_FILES)],
    scopes: Annotated[list[str], Form(description=constants.ADD_SCOPES)],
    request: Request = None,
):
    return upload_file_ser(files=files, scopes=scopes, request=request)


@router.post("/upload-image/", status_code=status.HTTP_201_CREATED)
def upload_image(image: UploadFile, request: Request = None):
    return upload_image_ser(image=image, request=request)


@router.post("/", status_code=status.HTTP_200_OK)
def read_files(filter: FileFilter):
    return get_files_ser(filter=filter)
