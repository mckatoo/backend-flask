import json
from uuid import uuid1

from database.models.users import Users
from tests.utils import generate_mocked_user_data


def test_unauthorized_error_on_request_without_valid_token(client):
    response = client.patch(
        "api/user/token",
        headers={"authentication": "Bearer invalid-token"},
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_update_user_and_return_204_status_code(client):
    random_id = uuid1()
    mocked_new_data = {"email": f"updated_{random_id}@email.com"}
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()
    response = client.patch(
        f"api/user/{existent_user.id}",
        headers={"authentication": f"Bearer {access_token}"},
        data=json.dumps(mocked_new_data),
        content_type="application/json",
    )
    updated_user = Users.get_by_id(existent_user.id)

    assert response.status_code == 204
    assert updated_user.email == mocked_new_data["email"]
    assert updated_user.verify_password(existent_user_data["password"])


def test_error_400_when_request_update_without_id(client):
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()
    response = client.patch(
        "api/user",
        headers={"authentication": f"Bearer {access_token}"},
        data=json.dumps({}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_error_400_when_request_update_without_data(client):
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()
    response = client.patch(
        "api/user",
        headers={"authentication": f"Bearer {access_token}"},
        content_type="application/json",
    )

    assert response.status_code == 400


def test_error_400_when_request_update_with_invalid_data(client):
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()
    response = client.patch(
        "api/user",
        headers={"authentication": f"Bearer {access_token}"},
        data=json.dumps({"invalid": "data"}),
        content_type="application/json",
    )

    assert response.status_code == 400
