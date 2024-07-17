from datetime import datetime, timedelta, timezone

import jwt

from configurations import envs_config
from database.models.users import Users
from tests.utils import generate_mocked_user_data


def test_success_on_refresh_token(client):
    mocked_user = generate_mocked_user_data()
    created_user = Users.create(**mocked_user)
    access_token = created_user.generate_tokens()[0]

    response = client.post(
        "api/auth/refresh-token",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json == {
        "username": created_user.username,
        "email": created_user.email,
    }


def test_fail_on_refresh_with_fake_token(client):
    access_token = jwt.encode(
        {
            "id": "fake_id",
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
        },
        envs_config.SECRET_KEY,
    )

    response = client.post(
        "api/auth/refresh-token",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}
