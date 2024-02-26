from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from src.apis.v1.models.auth import ConsumerAuthRequest
from src.apis.v1.models.auth import Token
from src.apis.v1.models.user import User
from src.apis.v1.service.auth import consumer_login_ser
from src.apis.v1.service.auth import get_login_user_or_consumer
from src.apis.v1.service.auth import login_for_access_token

router = APIRouter(redirect_slashes=False)


@router.post("/", response_model=Token, status_code=status.HTTP_201_CREATED)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    return login_for_access_token(form_data=form_data)


@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
def consumer_login(auth: ConsumerAuthRequest) -> Token:
    return consumer_login_ser(auth=auth)


@router.get("/user/me/", response_model=User, status_code=status.HTTP_200_OK)
def read_users_me(current_user: Annotated[User, Depends(get_login_user_or_consumer)]):
    return current_user
