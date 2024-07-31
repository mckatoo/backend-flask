from database.models.blacklist import Blacklist
from database.models.users import Users
from tests.utils import generate_mocked_user_data
import json


def test_when_sigout_return_200_status_code_and_add_on_blacklist(client):
    mocked_user = generate_mocked_user_data()
    user = Users.create(**mocked_user)
    access_token = user.generate_tokens()["access_token"]

    response = client.post(
        "api/auth/sign-out",
        headers={"authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )
    blacklist_token = Blacklist.get_or_none(Blacklist.token == access_token)

    assert response.status_code == 200
    assert blacklist_token is not None


def test_should_return_401_status_code_when_request_restrict_route_after_signout(
    client,
):
    mocked_user = generate_mocked_user_data()
    user = Users.create(**mocked_user)
    access_token = user.generate_tokens()["access_token"]

    success_response = client.post(
        "api/user",
        data=json.dumps(generate_mocked_user_data()),
        headers={"authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )
    assert success_response.status_code == 201

    client.post(
        "api/auth/sign-out",
        headers={"authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    response = client.post(
        "api/user",
        data=json.dumps(generate_mocked_user_data()),
        headers={"authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    assert response.status_code == 401
