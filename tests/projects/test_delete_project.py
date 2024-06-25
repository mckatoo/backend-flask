from uuid import uuid1

from playhouse.shortcuts import dict_to_model

from database.models.projects import Projects


def test_delete_project(client):
    random_id = uuid1()
    mocked_data = {
        "title": f"Title test {random_id}",
        "description": f"Description test  {random_id}",
        "snapshot": f"http://snapshot.com/image-{random_id}.jpg",
        "repository_link": f"http://repository.com/my{random_id}.git",
        "start": "2024/03/22",
        "last_update": "2024/06/13",
    }
    project = dict_to_model(Projects, mocked_data)
    project.save()
    id = project.get_id()
    response = client.delete(
        f"api/project/{id}", content_type="application/json"
    )

    assert response.status_code == 204
    assert not Projects.get_or_none(Projects.id == id)


def test_error_when_request_without_id(client):
    response = client.delete(
        "api/project",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
