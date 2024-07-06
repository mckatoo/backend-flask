import json
from unittest.mock import patch
from tests.utils import generate_mocked_user_data
from database.models.users import Users


mocked_user = generate_mocked_user_data()
access_token, _ = Users.create(**mocked_user).generate_tokens()


@patch("smtplib.SMTP")
def test_unauthorized_error_on_request_without_valid_token(mock, client):
    mocked_request = json.dumps(
        {
            "from": "sender@mail.com",
            "to": "reciper@mail.com",
            "message": "hello",
        }
    )
    response = client.post(
        "api/mailer",
        headers={"authentication": "Bearer invalid-token"},
        data=mocked_request,
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


@patch("smtplib.SMTP")
def test_send_mail_returning_status_201_and_json(mock, client):
    mocked_request = json.dumps(
        {
            "from": "sender@mail.com",
            "to": "reciper@mail.com",
            "message": "hello",
        }
    )
    response = client.post(
        "api/mailer",
        headers={"authentication": f"Bearer {access_token}"},
        data=mocked_request,
        content_type="application/json",
    )

    assert response.status_code == 201


def test_send_mail_with_invalid_data_returning_status_400_and_json(client):
    mocked_request = json.dumps(
        {
            "invalid": "data",
        }
    )
    response = client.post(
        "api/mailer",
        headers={"authentication": f"Bearer {access_token}"},
        data=mocked_request,
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}


def test_send_mail_without_data_returning_status_400_and_json(client):
    response = client.post(
        "api/mailer",
        headers={"authentication": f"Bearer {access_token}"},
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
