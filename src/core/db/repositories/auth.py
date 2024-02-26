import hashlib
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import jwt
from sqlalchemy.orm import Session

from src.apis.v1.models.auth import ConsumerAuthRequest
from src.core.config.settings import settings
from src.core.db.models.consumer import Consumer
from src.core.db.models.user import User


def authenticate_username(db: Session, username: str):
    user: User = get_user(db, username)
    if not user:
        return False
    return user


def authenticate_password(password: str, hashed_password: str):
    if not verify_password(password, hashed_password):
        return False
    return True


def get_user(db: Session, username: str):
    user: User = db.query(User).filter(User.username == username).one_or_none()
    return user


def verify_password(plain_password: str, hashed_password: str):
    hash_object = hashlib.sha256(plain_password.encode("utf-8"))
    hash_password = "0x" + hash_object.hexdigest().upper()
    if hashed_password == hash_password:
        return True
    return False


def create_user_access_token(user: User):
    data = {
        "username": user.username,
        "info": settings.HEX32_OPENSSL_TOKEN_INFO,
        "from": settings.HEX32_OPENSSL_TOKEN_FORM,
    }
    return create_jwt_token(data)


def create_consumer_access_token(consumer: Consumer, auth: ConsumerAuthRequest):
    data = {
        "consumer": consumer.consumer_id,
        "info": settings.HEX32_OPENSSL_TOKEN_INFO,
        "from": settings.HEX32_OPENSSL_TOKEN_FORM,
        "scopes": auth.scopes,
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
