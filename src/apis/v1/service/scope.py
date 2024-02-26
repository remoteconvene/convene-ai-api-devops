from src.apis.v1.models.scope import ScopeRequest
from src.apis.v1.models.scope import ScopeRequestUpdate
from src.core.db.repositories.scope import add_scope_repo
from src.core.db.repositories.scope import delete_scope_repo
from src.core.db.repositories.scope import get_scope_repo
from src.core.db.repositories.scope import get_scopes_repo
from src.core.db.repositories.scope import update_scope_repo


def add_scope_ser(scope: ScopeRequest):
    return add_scope_repo(scope=scope)


def update_scope_ser(id: int, scope: ScopeRequestUpdate):
    return update_scope_repo(id, scope=scope)


def delete_scope_ser(id: int):
    return delete_scope_repo(id=id)


def get_scopes_ser():
    return get_scopes_repo()


def get_scope_ser(id: int):
    return get_scope_repo(id=id)
