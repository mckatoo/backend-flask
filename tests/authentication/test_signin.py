from uuid import uuid1
from flask import json
from configurations import envs_config
from database.models.users import Users
import jwt


def test_success_on_signin(client):
    random_id = uuid1()
    mocked_user = {
        "email": f"user{random_id}@mail.com",
        "password": "123456",
    }
    created_user = Users.create(
        username=f"user_name {random_id}", **mocked_user
    )

    response = client.post(
        "api/auth/sign-in",
        data=json.dumps(mocked_user),
        content_type="application/json",
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
