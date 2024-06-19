import json
from unittest.mock import patch

def test_send_mail_returning_status_201_and_json(client):
    patch("configurations.mail_config.send_mail")
    mocked_request = json.dumps(
        {
            "from": "sender@mail.com",
            "to": "reciper@mail.com",
            "message": "hello",
        }
    )
    response = client.post(
        "api/mailer", data=mocked_request, content_type="application/json"
    )

    assert response.status_code == 201


# def test_send_mail_with_invalid_data_returning_status_404_and_json(client):
#     response = client.post("api/mailer", content_type="application/json")

#     assert response.status_code == 201
