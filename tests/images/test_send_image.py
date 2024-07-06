import io
from unittest.mock import Mock
import cloudinary.uploader as uploader
from tests.utils import generate_mocked_user_data
from database.models.users import Users


mocked_user = Users.create(**generate_mocked_user_data())
access_token, _ = mocked_user.generate_tokens()


def test_unauthorized_error_on_request_without_valid_token(client):
    mocked_result = {
        "public_id": "test_public_id",
        "secure_url": "test_secure_url",
    }
    data = {"file": (io.BytesIO(b"some initial text data"), "teste.jpg")}
    uploader.upload = Mock(return_value=mocked_result)
    response = client.post(
        "api/image",
        headers={"authentication": "Bearer invalid-token"},
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_send_image_returning_status_201_and_json(client):
    mocked_result = {
        "public_id": "test_public_id",
        "secure_url": "test_secure_url",
    }
    data = {"file": (io.BytesIO(b"some initial text data"), "teste.jpg")}
    uploader.upload = Mock(return_value=mocked_result)
    response = client.post(
        "api/image",
        headers={"authentication": f"Bearer {access_token}"},
        data=data,
        content_type="multipart/form-data",
    )

    assert uploader.upload.called
    assert response.json == {
        "publicId": mocked_result["public_id"],
        "url": mocked_result["secure_url"],
    }
    assert response.status_code == 201


def test_send_without_image_returning_status_400_and_json(client):
    response = client.post(
        "api/image",
        headers={"authentication": f"Bearer {access_token}"},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.json == {"error": "No file part"}


def test_send_invalid_image_returning_status_400_and_json(client):
    mocked_data = {
        "file": (io.BytesIO(b"some initial text data"), "invalid.image")
    }
    response = client.post(
        "api/image",
        headers={"authentication": f"Bearer {access_token}"},
        data=mocked_data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Not allowed file"}


def test_send_empty_image_returning_status_400_and_json(client):
    mocked_data = {"file": (io.BytesIO(b"some initial text data"), "")}
    response = client.post(
        "api/image",
        headers={"authentication": f"Bearer {access_token}"},
        data=mocked_data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.json == {"error": "No selected file"}
