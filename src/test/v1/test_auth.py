from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.apis.v1.models.auth import ConsumerAuthRequest
from src.core.config.settings import settings
from src.core.utils.error_messages import errors
from src.core.utils.messages import messages
from src.test.v1.test_variables import values


api_route = settings.API_PREFIX + settings.CURRENT_API_VERSION + "/auth"


auth_data: Annotated[OAuth2PasswordRequestForm, Depends()] = {
    "username": values.USERNAME,
    "password": values.PASSWORD,
    "grant_type": values.GRANT_TYPE,
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}


def test_auth_login(client):
    response = client.post(
        api_route,
        headers=headers,
        data=auth_data,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["token_type"] == messages.BEARER
    assert "access_token" in data


invalid_username_data: Annotated[OAuth2PasswordRequestForm, Depends()] = {
    "username": values.INCORRECT_USERNAME,
    "password": values.PASSWORD,
    "grant_type": values.GRANT_TYPE,
}


def test_invalid_username(client):
    response = client.post(
        api_route,
        headers=headers,
        data=invalid_username_data,
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == errors.INVALID_USERNAME + invalid_username_data["username"]


invalid_password_data: Annotated[OAuth2PasswordRequestForm, Depends()] = {
    "username": values.USERNAME,
    "password": values.INCORRECT_PASSWORD,
    "grant_type": values.GRANT_TYPE,
}


def test_incorrect_password(client):
    response = client.post(
        api_route,
        headers=headers,
        data=invalid_password_data,
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == errors.INCORRECT_PASSWORD


disabled_user_data: Annotated[OAuth2PasswordRequestForm, Depends()] = {
    "username": values.BLOCKED_USERNAME,
    "password": values.PASSWORD,
    "grant_type": values.GRANT_TYPE,
}


def test_disable_user(client):
    response = client.post(
        api_route,
        headers=headers,
        data=disabled_user_data,
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == errors.BLOCKED_USERNAME


token = values.TOKEN
scopes = values.SCOPES

consumer_login_data: ConsumerAuthRequest = {
    "consumer_id": values.CONSUMER_ID,
    "jwt_token": token,
    "scopes": scopes,
}


def test_consumer_login(client):
    response = client.post(
        f"{api_route}/login",
        json=consumer_login_data,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == messages.BEARER
    assert "access_token" in data


invalid_consumer_login_data: ConsumerAuthRequest = {
    "consumer_id": values.INCORRECT_CONSUMER_ID,
    "jwt_token": token,
    "scopes": scopes,
}


def test_invaid_consumer_login(client):
    response = client.post(
        f"{api_route}/login",
        json=invalid_consumer_login_data,
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == errors.INVALID_CONSUMER


disabled_consumer_login_data: ConsumerAuthRequest = {
    "consumer_id": values.BLOCKED_CONSUMER_ID,
    "jwt_token": token,
    "scopes": scopes,
}


def test_disabled_consumer_login(client):
    response = client.post(
        f"{api_route}/login",
        json=disabled_consumer_login_data,
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == errors.BLOCKED_CONSUMER
