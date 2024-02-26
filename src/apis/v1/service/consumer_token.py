from jose import jwt

from src.apis.v1.enums.auth_type import AuthType
from src.apis.v1.enums.token_data import TokenData
from src.core.config.settings import settings
from src.core.db.models.consumer import Consumer
from src.core.db.models.user import User
from src.core.db.repositories.consumer import get_consumer
from src.core.db.repositories.consumer_token import get_consumer_token
from src.core.db.repositories.user import get_user


def get_token_detail(token: str):
    payload = jwt.decode(
        token,
        settings.HEX32_OPENSSL_SECRET_KEY,
        algorithms=[settings.HEX32_OPENSSL_ALGORITHM],
    )

    username: str = payload.get(AuthType.USERNAME_LOGIN.value)
    consumer_id: str = payload.get(AuthType.CONSUMER_LOGIN.value)

    if username is not None:
        user: User = get_user(username=username)

    if consumer_id is not None:
        consumer: Consumer = get_consumer(consumer_id=consumer_id)
        consumer_token = get_consumer_token(consumer_id=consumer.id, jwt_token=token)

    _consumer_id = None
    if consumer_id is not None:
        _consumer_id = consumer_token.consumer_id

    external_user_id = None
    if consumer_id is not None:
        external_user_id = consumer_token.id

    scopes = None
    if consumer_id is not None:
        scopes = consumer_token.scopes

    user_id = None
    if username is not None:
        user_id = user.id
        external_user_id = user.id

    return {
        TokenData.CONSUMER_ID: _consumer_id,
        TokenData.EXTERNAL_USER_ID: external_user_id,
        TokenData.USER_ID: user_id,
        TokenData.SCOPES: scopes,
    }
