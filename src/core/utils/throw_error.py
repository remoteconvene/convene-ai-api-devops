from fastapi import HTTPException


def raise_error(status_code: int, detail: str, headers: object = None):
    raise HTTPException(status_code=status_code, detail=detail, headers=headers)
