from typing import Union
from uuid import UUID

from src.core.utils.custom_errors import InvalidUuidError
from src.core.utils.error_messages import errors


def validate_uuid(uuid: Union[str, UUID]) -> None:
    try:
        uuid_obj = UUID(str(uuid))
    except ValueError as e:
        raise InvalidUuidError(errors.INVALID_UUID) from e

    if uuid_obj.version != 4:
        raise InvalidUuidError(errors.INVALID_UUID_4)
