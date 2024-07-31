from datetime import datetime, timedelta, timezone

import jwt

from configurations import envs_config
from database.models.users import Users
from middlewares.verify_token import decode_token
from tests.utils import generate_mocked_user_data


def test_success_on_refresh_token(client):
    mocked_user = generate_mocked_user_data()
    created_user = Users.create(**mocked_user)
    tokens = created_user.generate_tokens()

    response = client.post(
        "api/auth/refresh-token",
        json={"refreshToken": tokens["refresh_token"]},
        headers={"authorization": f"Bearer {tokens["access_token"]}"},
    )
    decoded_access_token = decode_token(response.json["accessToken"])
    decoded_refresh_token = decode_token(response.json["refreshToken"])

    assert response.status_code == 200
    assert response.json["user"] == {
        "id": created_user.id,
        "username": created_user.username,
        "email": created_user.email,
    }
    assert decoded_access_token["exp"] == int(
        (datetime.now(tz=timezone.utc) + timedelta(minutes=10)).timestamp()
    )
    assert decoded_refresh_token["exp"] == int(
        (datetime.now(tz=timezone.utc) + timedelta(minutes=60)).timestamp()
    )


def test_fail_on_refresh_with_fake_refresh_token(client):
    mocked_user = generate_mocked_user_data()
    created_user = Users.create(**mocked_user)
    tokens = created_user.generate_tokens()
    refresh_token = jwt.encode(
        {
            "id": "fake_id",
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=60),
            "type": "refreshToken",
        },
        envs_config.SECRET_KEY,
    )

    response = client.post(
        "api/auth/refresh-token",
        json={"refreshToken": refresh_token},
        headers={"authorization": f"Bearer {tokens["access_token"]}"},
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_fail_on_refresh_with_access_token(client):
    mocked_user = generate_mocked_user_data()
    created_user = Users.create(**mocked_user)
    access_token = created_user.generate_access_token()
    response = client.post(
        "api/auth/refresh-token",
        json={"refreshToken": access_token},
        headers={"authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}
