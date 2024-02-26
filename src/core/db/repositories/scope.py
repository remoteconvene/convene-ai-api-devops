from fastapi import HTTPException
from fastapi import status

from src.apis.v1.enums.status_type import StatusType
from src.apis.v1.models.scope import ScopeRequest
from src.apis.v1.models.scope import ScopeRequestUpdate
from src.core.db.models.scope import Scope
from src.core.db.sql_session_manager import get_db
from src.core.utils.error_messages import errors


def add_scope_repo(scope: ScopeRequest):
    with get_db() as db:
        scope = Scope(name=scope.name, description=scope.description, status=True)
        db.add(scope)
        db.commit()
        db.refresh(scope)
        return scope


def update_scope_repo(id: int, scope: ScopeRequestUpdate):
    with get_db() as db:
        _scope = db.get(Scope, id)
        if not _scope:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=errors.NO_SCOPE_FOUND
            )

        _scope.name = scope.name
        _scope.description = scope.description
        _scope.status = scope.status
        db.commit()
        db.refresh(_scope)

        return _scope


def delete_scope_repo(id: int):
    with get_db() as db:
        scope = db.get(Scope, id)
        if not scope:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=errors.NO_SCOPE_FOUND
            )
        db.delete(scope)
        db.commit()


def get_scopes_repo():
    with get_db() as db:
        return db.query(Scope).filter(Scope.status == StatusType.ACTIVE.value).all()


def get_scope_repo(id: int):
    with get_db() as db:
        scope = db.get(Scope, id)
        if not scope:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=errors.NO_SCOPE_FOUND
            )
        return scope


def get_scopes(scopes: list[str]):
    with get_db() as db:
        consumer = db.query(Scope).filter(Scope.name.in_(scopes)).all()
        return consumer
