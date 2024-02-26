from pydantic import BaseModel


class User(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    username: str
    hashed_password: str
    superadmin: bool | None = None
    status: bool | None = None
    jwt_token: str = None
