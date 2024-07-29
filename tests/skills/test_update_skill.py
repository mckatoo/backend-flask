import json
import uuid

from playhouse.shortcuts import dict_to_model, model_to_dict

from database.models.skills import Skills
from database.models.users import Users
from tests.utils import generate_mocked_user_data

access_token = Users.create(**generate_mocked_user_data()).generate_tokens()["access_token"]


def test_unauthorized_error_on_request_without_valid_token(client):
    random_id = uuid.uuid1()
    mocked_data = {
        "title": f"Title test {random_id}",
    }
    mocked_new_data = {"title": f"EDITED - New Title {random_id}"}
    skill = dict_to_model(Skills, mocked_data)
    skill.save()
    id = skill.get_id()
    response = client.patch(
        f"api/skill/{id}",
        headers={"authentication": "Bearer invalid-token"},
        data=json.dumps(mocked_new_data),
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_update_skill_returning_status_204(client):
    random_id = uuid.uuid1()
    mocked_data = {
        "title": f"Title test {random_id}",
    }
    mocked_new_data = {"title": f"EDITED - New Title {random_id}"}
    skill = dict_to_model(Skills, mocked_data)
    skill.save()
    id = skill.get_id()
    response = client.patch(
        f"api/skill/{id}",
        data=json.dumps(mocked_new_data),
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )
    updated_skill = Skills.get_by_id(id)
    for key in mocked_new_data:
        mocked_data[key] = mocked_new_data[key]

    assert response.status_code == 204
    assert model_to_dict(updated_skill) == {"id": id, **mocked_data}


def test_error_when_request_without_new_data(client):
    random_id = uuid.uuid1()
    response = client.patch(
        f"api/skill/{random_id}",
        headers={"authentication": f"Bearer {access_token}"},
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}


def test_error_when_request_without_id(client):
    random_id = uuid.uuid1()
    mocked_data = {
        "title": f"Title test {random_id}",
    }
    response = client.patch(
        "api/skill",
        data=json.dumps(mocked_data),
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}


def test_error_when_request_with_not_founded_id(client):
    random_id = uuid.uuid1()
    response = client.patch(
        f"api/skill/{random_id}",
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
