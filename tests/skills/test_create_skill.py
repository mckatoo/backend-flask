import json
from uuid import uuid1

from database.models.skills import Skills
from database.models.users import Users
from tests.utils import generate_mocked_user_data

access_token = Users.create(**generate_mocked_user_data()).generate_tokens()["access_token"]


def test_unauthorized_error_on_request_without_valid_token(client):
    random_id = uuid1()
    mocked_data = {"title": f"Title test {random_id}"}
    response = client.post(
        "api/skill",
        headers={"authorization": "Bearer invalid-token"},
        data=json.dumps(mocked_data),
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_create_skill(client):
    random_id = uuid1()
    mocked_data = {"title": f"Title test {random_id}"}
    response = client.post(
        "api/skill",
        data=json.dumps(mocked_data),
        content_type="application/json",
        headers={"authorization": f"Bearer {access_token}"},
    )
    created_skill = Skills.get_or_none(Skills.title == mocked_data["title"])

    assert response.status_code == 201
    assert response.json == {"id": created_skill.id}


def test_error_on_request_without_data(client):
    response = client.post(
        "api/skill",
        content_type="application/json",
        headers={"authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}


def test_error_on_request_with_invalid_data(client):
    mocked_data = {"invalid": "data"}
    response = client.post(
        "api/skill",
        data=json.dumps(mocked_data),
        content_type="application/json",
        headers={"authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
