import io
import json
from unittest.mock import Mock

import cloudinary.uploader as uploader
import cloudinary.api as api


def test_send_image_returning_status_201_and_json(client):
    mocked_result = {
        "public_id": "test_public_id",
        "secure_url": "test_secure_url",
    }
    data = {"file": (io.BytesIO(b"some initial text data"), "teste.jpg")}
    uploader.upload = Mock(return_value=mocked_result)
    response = client.post(
        "api/image", data=data, content_type="multipart/form-data"
    )

    assert uploader.upload.called
    assert response.json == {
        "publicId": mocked_result["public_id"],
        "url": mocked_result["secure_url"],
    }
    assert response.status_code == 201


def test_get_image_returning_status_200_and_json(client):
    mocked_request = json.dumps(dict(id="mocked_public_id"))
    mocked_response = {"url": "http://mocked.com/response.jpg"}
    api.resource = Mock(return_value=mocked_response)
    response = client.get(
        "api/image", data=mocked_request, content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json == {"url": mocked_response["url"]}


def test_get_without_id_return_error_and_status_400(client):
    response = client.get("api/image", content_type="application/json")

    assert response.status_code == 400
    assert response.json == {"error": "No id"}


def test_get_with_invalid_id_return_error_and_status_400(client):
    mocked_request = json.dumps(dict(id="mocked_public_id"))
    mocked_response = "NotFound('Error 404 - Resource not found - mocked_public_id')"
    api.resource = Mock(side_effect=Exception(mocked_response))
    response = client.get(
        "api/image", data=mocked_request, content_type="application/json"
    )

    assert response.status_code == 404
    assert response.json == {"error": "Image not found"}

def test_on_try_get_with_unexpected_error_return_error_and_status_500(client):
    mocked_request = json.dumps(dict(id="mocked_public_id"))
    mocked_response = "Unexpected error"
    api.resource = Mock(side_effect=Exception(mocked_response))
    response = client.get(
        "api/image", data=mocked_request, content_type="application/json"
    )

    assert response.status_code == 500
    assert response.json == {"error": "Unexpected error"}


def test_delete_image_returning_status_204_and_no_content(client):
    uploader.destroy = Mock()
    mocked_request = json.dumps(dict(id="mocked_public_id"))
    response = client.delete(
        "api/image", data=mocked_request, content_type="application/json"
    )

    assert response.status_code == 204
