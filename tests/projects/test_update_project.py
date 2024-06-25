import json
import uuid

from playhouse.shortcuts import dict_to_model, model_to_dict

from database.models.projects import Projects


def test_update_project_returning_status_204(client):
    random_id = uuid.uuid1()
    mocked_data = {
        "title": f"Title test {random_id}",
        "description": f"Description test  {random_id}",
        "snapshot": f"http://snapshot.com/image-{random_id}.jpg",
        "repository_link": f"http://repository.com/my{random_id}.git",
        "start": "2024/03/22",
        "last_update": "2024/06/13",
    }
    mocked_new_data = {"title": f"EDITED - New Title {random_id}"}
    project = dict_to_model(Projects, mocked_data)
    project.save()
    id = project.get_id()
    response = client.patch(
        f"api/project/{id}",
        data=json.dumps(mocked_new_data),
        content_type="application/json",
    )
    updated_project = Projects.get_by_id(id)
    for key in mocked_new_data:
        mocked_data[key] = mocked_new_data[key]

    assert response.status_code == 204
    assert model_to_dict(updated_project) == {"id": id, **mocked_data}


def test_error_when_request_without_new_data(client):
    random_id = uuid.uuid1()
    response = client.patch(
        f"api/project/{random_id}",
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
        "api/project",
        data=json.dumps(mocked_data),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}


def test_error_when_request_with_not_founded_id(client):
    random_id = uuid.uuid1()
    response = client.patch(
        f"api/project/{random_id}",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
