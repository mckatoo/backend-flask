import json
from unittest.mock import patch

from database.models.users import Users
from tests.utils import generate_mocked_user_data


@patch("smtplib.SMTP")
def test_recovery_password_with_status_200(mock, client):
    mocked_user = generate_mocked_user_data()
    Users.create(**mocked_user)
    response = client.post(
        "api/user/recovery-password",
        data=json.dumps({"email": mocked_user["email"]}),
        content_type="application/json",
    )
    user = Users.get(Users.email == mocked_user["email"])

    assert response.status_code == 204
    assert not user.verify_password(mocked_user["password"])


def test_fail_with_status_404_on_use_invalid_email(client):
    response = client.post(
        "api/user/recovery-password",
        data=json.dumps({"email": "invalid@email.com"}),
        content_type="application/json",
    )

    assert response.status_code == 404
