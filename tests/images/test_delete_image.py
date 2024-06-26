import json
from unittest.mock import Mock

import cloudinary.uploader as uploader


def test_delete_image_returning_status_204_and_no_content(client):
    uploader.destroy = Mock()
    mocked_request = json.dumps(dict(id="mocked_public_id"))
    response = client.delete(
        "api/image", data=mocked_request, content_type="application/json"
    )

    assert response.status_code == 204

def test_delete_without_image_returning_status_400_and_json(client):
    response = client.delete(
        "api/image", content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json == {"error": "No id"}
