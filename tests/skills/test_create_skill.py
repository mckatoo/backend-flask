import json
from uuid import uuid1

from database.models.skills import Skills


def test_create_skill(client):
    random_id = uuid1()
    mocked_data = {"title": f"Title test {random_id}"}
    response = client.post(
        "api/skill",
        data=json.dumps(mocked_data),
        content_type="application/json",
    )
    created_skill = Skills.get_or_none(Skills.title == mocked_data["title"])

    assert response.status_code == 201
    assert response.json == {"id": created_skill.id}


def test_error_on_request_without_data(client):
    response = client.post(
        "api/skill",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}


def test_error_on_request_with_invalid_data(client):
    mocked_data = {"invalid": "data"}
    response = client.post(
        "api/skill",
        data=json.dumps(mocked_data),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
