import json
import cloudinary.api as api
from unittest.mock import Mock


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
    mocked_response = (
        "NotFound('Error 404 - Resource not found - mocked_public_id')"
    )
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
