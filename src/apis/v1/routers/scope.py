from typing import List

from fastapi import APIRouter
from fastapi import status

from src.apis.v1.models.scope import ScopeRequest
from src.apis.v1.models.scope import ScopeRequestUpdate
from src.apis.v1.models.scope import ScopeResponse
from src.apis.v1.service.scope import add_scope_ser
from src.apis.v1.service.scope import delete_scope_ser
from src.apis.v1.service.scope import get_scope_ser
from src.apis.v1.service.scope import get_scopes_ser
from src.apis.v1.service.scope import update_scope_ser

router = APIRouter(redirect_slashes=False)


@router.post(
    "/",
    response_model=ScopeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_scope(scope: ScopeRequest):
    return add_scope_ser(scope=scope)


@router.put(
    "/{id}",
    response_model=ScopeResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_scope(id: int, scope: ScopeRequestUpdate):
    return update_scope_ser(id, scope=scope)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_scope(id: int):
    return delete_scope_ser(id=id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ScopeResponse])
def read_scopes():
    return get_scopes_ser()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ScopeResponse)
def read_scope(id: int):
    return get_scope_ser(id=id)
