from datetime import datetime, timedelta, timezone
from uuid import uuid1

import jwt

from configurations import envs_config
from database.models.blacklist import Blacklist
from database.models.users import Users


def test_when_sigout_return_200_status_code_and_add_on_blacklist(client):
    random_id = uuid1()
    mocked_user = {
        "username": f"user_{random_id}",
        "email": f"user{random_id}@mail.com",
        "password": "123456",
    }
    user = Users.create(**mocked_user)

    access_token = jwt.encode(
        {
            "id": user.id,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
        },
        envs_config.SECRET_KEY,
    )
    response = client.post(
        "api/auth/sign-out",
        headers={"authentication": f"Bearer {access_token}"},
        content_type="application/json",
    )
    blacklist_token = Blacklist.get_or_none(Blacklist.token == access_token)

    assert response.status_code == 200
    assert blacklist_token is not None


def test_should_return_401_status_code_when_request_restrict_route_after_signout(
    client,
):
    response = client.post(
        "/api/user",
        content_type="application/json",
    )

    assert response.status_code == 401
