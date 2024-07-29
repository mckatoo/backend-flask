import json
from unittest.mock import patch

from database.models.users import Users
from tests.utils import generate_mocked_user_data


mocked_user = Users.create(**generate_mocked_user_data())
access_token = mocked_user.generate_tokens()["access_token"]


@patch("cloudinary.uploader")
def test_unauthorized_error_on_request_without_valid_token(mock, client):
    mocked_request = json.dumps(dict(id="mocked_public_id"))
    response = client.delete(
        "api/image",
        headers={"authentication": "Bearer invalid-token"},
        data=mocked_request,
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


@patch("cloudinary.uploader")
def test_delete_image_returning_status_204_and_no_content(mock, client):
    mocked_request = json.dumps(dict(id="mocked_public_id"))
    response = client.delete(
        "api/image",
        data=mocked_request,
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 204


@patch("cloudinary.uploader")
def test_delete_without_image_returning_status_400_and_json(mock, client):
    response = client.delete(
        "api/image",
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "No id"}
