import io
from unittest import mock


@mock.patch(
    "cloudinary.uploader.upload",
    # {"public_id": "test_public_id", "secure_url": "test_secure_url"},
)
def test_send_image_returning_status_201_and_json(client):
    data = {"name": "this is a name", "age": 12}
    data = {key: str(value) for key, value in data.items()}
    data["file"] = (io.BytesIO(b"abcdef"), "test.jpg")  # type: ignore
    response = client.post(
        "api/image", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 201
    assert response.json == {
        "url": "secure_url",
        "publicId": "public_id",
    }


def test_get_image_returning_status_200_and_json(client):
    response = client.get("api/image")
    assert response.status_code == 200
    assert response.json == {"url": "url"}


def test_delete_image_returning_status_204_and_no_content(client):
    response = client.delete("api/image")
    assert response.status_code == 204
