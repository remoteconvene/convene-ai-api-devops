import hashlib
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError

from src.apis.v1.models.auth import ConsumerAuthRequest
from src.apis.v1.models.auth import Token
from src.apis.v1.models.user import User
from src.core.config.settings import settings
from src.core.db.models.consumer import Consumer
from src.core.db.repositories.consumer import get_consumer
from src.core.db.repositories.consumer_token import update_consumer_token
from src.core.db.repositories.scope import get_scopes
from src.core.db.repositories.user import get_user
from src.core.db.repositories.user import update_user_token
from src.core.utils.error_messages import errors
from src.core.utils.messages import messages
from src.core.utils.throw_error import raise_error

tokenUrl = settings.API_PREFIX + settings.CURRENT_API_VERSION + "/auth/"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=tokenUrl)
headers = {"WWW-Authenticate": "Bearer"}


def get_login_user_or_consumer(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=errors.INVALID_TOKEN,
        headers=headers,
    )
    try:
        payload = jwt.decode(
            token,
            settings.HEX32_OPENSSL_SECRET_KEY,
            algorithms=[settings.HEX32_OPENSSL_ALGORITHM],
        )

        username: str = payload.get("username")
        consumer_id: str = payload.get("consumer")

        if username is None and consumer_id is None:
            raise credentials_exception

        if username is not None:
            user = get_user(username=username)

            if user is None:
                raise credentials_exception

            return user

        if consumer_id is not None:
            consumer = get_consumer(consumer_id=consumer_id)
            token_scopes: str = payload.get("scopes")
            scopes = get_scopes(scopes=token_scopes)

            for scope in scopes:
                if scope.status is not True:
                    raise_error(
                        status.HTTP_401_UNAUTHORIZED,
                        errors.TOKEN_SCOPE_DISABLED,
                        headers,
                    )

            if consumer is None:
                raise credentials_exception

            return consumer

    except JWTError:
        raise credentials_exception


def get_user_or_consumer(model: Annotated[any, Depends(get_login_user_or_consumer)]):
    if model is not None:
        if not model.status:
            raise_error(
                status.HTTP_400_BAD_REQUEST,
                errors.INACTIVE,
            )
    return model


def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user: User = get_user(form_data.username)
    if not user:
        raise_error(
            status.HTTP_401_UNAUTHORIZED,
            errors.INVALID_USERNAME + form_data.username,
            headers=headers,
        )

    is_pass_matched = authenticate_password(form_data.password, user.hashed_password)
    if not is_pass_matched:
        raise_error(
            status.HTTP_401_UNAUTHORIZED,
            errors.INCORRECT_PASSWORD,
            headers=headers,
        )

    if user.status is not True:
        raise_error(
            status.HTTP_401_UNAUTHORIZED,
            errors.BLOCKED_USERNAME,
            headers=headers,
        )

    access_token = create_user_access_token(user)
    update_user_token(user.username, access_token)
    return Token(access_token=access_token, token_type=messages.BEARER)


def consumer_login_ser(auth: ConsumerAuthRequest) -> Token:
    consumer = get_consumer(consumer_id=auth.consumer_id)
    if consumer is None:
        raise_error(
            status.HTTP_401_UNAUTHORIZED,
            errors.INVALID_CONSUMER,
            headers=headers,
        )

    if consumer.status is not True:
        raise_error(
            status.HTTP_401_UNAUTHORIZED,
            errors.BLOCKED_CONSUMER,
            headers=headers,
        )

    scopes = get_scopes(scopes=auth.scopes)
    if scopes is None:
        raise_error(
            status.HTTP_401_UNAUTHORIZED,
            errors.INVALID_SCOPE,
            headers=headers,
        )

    for scope in scopes:
        if scope.status is not True:
            raise_error(
                status.HTTP_401_UNAUTHORIZED,
                errors.BLOCKED_SCOPE,
                headers=headers,
            )

    access_token = create_consumer_access_token(consumer, auth)
    update_consumer_token(consumer, auth, access_token)
    return Token(access_token=access_token, token_type=messages.BEARER)


def authenticate_password(password: str, hashed_password: str):
    if not verify_password(password, hashed_password):
        return False
    return True


def verify_password(plain_password: str, hashed_password: str):
    hash_password = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    if hashed_password == hash_password:
        return True
    return False


def create_user_access_token(user: User):
    data = {
        "username": user.username,
        "info": settings.HEX32_OPENSSL_TOKEN_INFO,
        "from": settings.HEX32_OPENSSL_TOKEN_FORM,
    }
    access_token = create_jwt_token(data)
    return access_token


def create_consumer_access_token(consumer: Consumer, auth: ConsumerAuthRequest):
    data = {
        "consumer": consumer.consumer_id,
        "info": settings.HEX32_OPENSSL_TOKEN_INFO,
        "from": settings.HEX32_OPENSSL_TOKEN_FORM,
        "scopes": auth.scopes,
        "email": auth.email,
        "auth_token": auth.jwt_token,
    }
    return create_jwt_token(data)


def create_jwt_token(data: any):
    access_token_expires = datetime.now(timezone.utc) + timedelta(
        minutes=int(settings.HEX32_OPENSSL_TOKEN_EXPIRY_MIN)
    )
    data.update({"exp": access_token_expires})
    encoded_jwt = jwt.encode(
        data,
        settings.HEX32_OPENSSL_SECRET_KEY,
        algorithm=settings.HEX32_OPENSSL_ALGORITHM,
    )
    return encoded_jwt
