from datetime import datetime, timedelta, timezone

import jwt
from flask import json

from configurations import envs_config
from database.models.users import Users
from tests.utils import generate_mocked_user_data


def test_success_on_signin_using_email(client):
    mocked_user = generate_mocked_user_data()
    created_user = Users.create(**mocked_user)

    response = client.post(
        "api/auth/sign-in",
        json={
            "email": mocked_user["email"],
            "password": mocked_user["password"],
        },
    )
    access_token = response.json["accessToken"]
    refresh_token = response.json["refreshToken"]
    access_token_payload = jwt.decode(
        access_token, envs_config.SECRET_KEY, algorithms="HS256"
    )
    refresh_token_payload = jwt.decode(
        refresh_token, envs_config.SECRET_KEY, algorithms="HS256"
    )

    assert response.status_code == 200
    assert access_token_payload["id"] == created_user.id
    assert refresh_token_payload["id"] == created_user.id
    assert access_token_payload["exp"] == int(
        (datetime.now(tz=timezone.utc) + timedelta(minutes=10)).timestamp()
    )
    assert refresh_token_payload["exp"] == int(
        (datetime.now(tz=timezone.utc) + timedelta(minutes=60)).timestamp()
    )


def test_success_on_signin_using_username(client):
    mocked_user = generate_mocked_user_data()
    created_user = Users.create(**mocked_user)

    response = client.post(
        "api/auth/sign-in",
        json={
            "username": mocked_user["username"],
            "password": mocked_user["password"],
        },
    )
    access_token = response.json["accessToken"]
    refresh_token = response.json["refreshToken"]
    access_token_payload = jwt.decode(
        access_token, envs_config.SECRET_KEY, algorithms="HS256"
    )
    refresh_token_payload = jwt.decode(
        refresh_token, envs_config.SECRET_KEY, algorithms="HS256"
    )

    assert response.status_code == 200
    assert access_token_payload["id"] == created_user.id
    assert refresh_token_payload["id"] == created_user.id
    assert access_token_payload["exp"] == int(
        (datetime.now(tz=timezone.utc) + timedelta(minutes=10)).timestamp()
    )
    assert refresh_token_payload["exp"] == int(
        (datetime.now(tz=timezone.utc) + timedelta(minutes=60)).timestamp()
    )


def test_fail_on_request_signin_with_invalid_credentials(client):
    mocked_user = {
        "email": "invalid@user.com",
        "password": "123456",
    }

    response = client.post(
        "api/auth/sign-in",
        data=json.dumps(mocked_user),
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_bad_request_error_when_request_without_credentials(client):
    response = client.post(
        "api/auth/sign-in",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
