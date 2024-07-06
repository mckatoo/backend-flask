from uuid import uuid1

from playhouse.shortcuts import dict_to_model

from database.models.skills import Skills
from database.models.users import Users
from tests.utils import generate_mocked_user_data

access_token, _ = Users.create(**generate_mocked_user_data()).generate_tokens()


def test_unauthorized_error_on_request_without_valid_token(client):
    random_id = uuid1()
    mocked_data = {
        "title": f"Title test {random_id}",
    }
    skill = dict_to_model(Skills, mocked_data)
    skill.save()
    id = skill.get_id()
    response = client.delete(
        f"api/skill/{id}",
        content_type="application/json",
        headers={"authentication": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_delete_skill(client):
    random_id = uuid1()
    mocked_data = {
        "title": f"Title test {random_id}",
    }
    skill = dict_to_model(Skills, mocked_data)
    skill.save()
    id = skill.get_id()
    response = client.delete(
        f"api/skill/{id}",
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 204
    assert not Skills.get_or_none(Skills.id == id)


def test_error_when_request_without_id(client):
    response = client.delete(
        "api/skill",
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
