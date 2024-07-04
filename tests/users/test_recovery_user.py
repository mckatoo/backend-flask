from tests.utils import generate_mocked_user_data
import json
from unittest.mock import patch


@patch("smtplib.SMTP")
def test_recovery_password_with_status_200(mock, client):
    mocked_user = generate_mocked_user_data()
    response = client.post(
        "api/user/recovery-password",
        data=json.dumps({"email": mocked_user["email"]}),
        content_type="application/json",
    )

    assert response.status_code == 200


def test_fail_with_status_404_on_use_invalid_email(client):
    assert False
