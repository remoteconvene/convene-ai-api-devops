from fastapi import Header
from fastapi import HTTPException
from fastapi import status

from src.core.utils.error_messages import errors


def request_id_required(x_request_id: str = Header(...)):
    if not x_request_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=errors.X_REQUEST_ID_REQUIRED
        )

    return x_request_id
