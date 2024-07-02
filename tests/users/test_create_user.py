import json

from database.models.users import Users
from tests.utils import generate_mocked_user_data


def test_create_user_returning_user_id_and_201_status_code(client):
    mocked_user_data = generate_mocked_user_data()
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()

    response = client.post(
        "api/user",
        data=json.dumps(mocked_user_data),
        headers={"authentication": f"Bearer {access_token}"},
        content_type="application/json",
    )
    created_user = Users.get(Users.email == mocked_user_data["email"])

    assert response.status_code == 201
    assert response.json == {"id": created_user.id}


def test_error_400_when_request_creation_without_data(client):
    assert False


def test_error_400_when_request_creation_with_invalid_data(client):
    assert False
