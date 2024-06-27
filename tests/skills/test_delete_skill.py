from uuid import uuid1

from playhouse.shortcuts import dict_to_model

from database.models.skills import Skills


def test_delete_skill(client):
    random_id = uuid1()
    mocked_data = {
        "title": f"Title test {random_id}",
    }
    skill = dict_to_model(Skills, mocked_data)
    skill.save()
    id = skill.get_id()
    response = client.delete(f"api/skill/{id}", content_type="application/json")

    assert response.status_code == 204
    assert not Skills.get_or_none(Skills.id == id)


def test_error_when_request_without_id(client):
    response = client.delete(
        "api/skill",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
