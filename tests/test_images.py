import io
from unittest.mock import Mock

import cloudinary.uploader as uploader
import cloudinary.api as api



def test_send_image_returning_status_201_and_json(client):
    mocked_result = {
        "public_id": "test_public_id",
        "secure_url": "test_secure_url",
    }
    mocked_value = {**mocked_result}
    mocked_value["file"] = (io.BytesIO(b"abcdef"), "test.jpg")  # type: ignore
    uploader.upload = Mock(return_value=mocked_value)
    response = client.post(
        "api/image", data=mocked_value, content_type="multipart/form-data"
    )

    assert uploader.upload.called
    assert response.json == {
        "publicId": mocked_result["public_id"],
        "url": mocked_result["secure_url"],
    }
    assert response.status_code == 201


def test_get_image_returning_status_200_and_json(client):
    mocked_request = {"id": "mocked_public_id"}
    mocked_response = {"url": "http://mocked.com/response.jpg"}
    api.resource = Mock(return_value = mocked_response)
    response = client.get("api/image",data=mocked_request, content_type="application/json")
    
    assert response.status_code == 200
    # assert response.json == {"url": mocked_response["url"]}


def test_delete_image_returning_status_204_and_no_content(client):
    response = client.delete("api/image")
    assert response.status_code == 204
