import json

from database.models.users import Users
from tests.utils import generate_mocked_user_data


def test_create_user_returning_user_id_and_201_status_code(client):
    mocked_user_data = generate_mocked_user_data()
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token = existent_user.generate_tokens()["access_token"]

    response = client.post(
        "api/user",
        data=json.dumps(mocked_user_data),
        headers={"authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )
    created_user = Users.get(Users.email == mocked_user_data["email"])

    assert response.status_code == 201
    assert response.json == {"id": created_user.id}


def test_error_400_when_request_creation_without_data(client):
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token = existent_user.generate_tokens()["access_token"]
    response = client.post(
        "api/user",
        headers={"authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}


def test_error_400_when_request_creation_with_invalid_data(client):
    mocked_user_data = generate_mocked_user_data()
    mocked_user_data.pop("email")
    mocked_user_data["invalid"] = "data"
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token = existent_user.generate_tokens()["access_token"]

    response = client.post(
        "api/user",
        data=json.dumps(mocked_user_data),
        headers={"authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
