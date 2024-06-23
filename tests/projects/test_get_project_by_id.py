import json
import uuid

from camel_converter import dict_to_camel
from playhouse.shortcuts import dict_to_model

from database.models.projects import Projects


def test_create_project_returning_status_201_and_id(client):
    random_id = uuid.uuid1()
    mocked_data = {
        "title": f"Title test {random_id}",
        "description": f"Description test  {random_id}",
        "snapshot": f"http://snapshot.com/image-{random_id}.jpg",
        "repositoryLink": f"http://repository.com/my{random_id}.git",
        "start": "2024/03/22",
        "lastUpdate": "2024/06/13",
    }
    response = client.post(
        "api/project",
        content_type="application/json",
        data=json.dumps(mocked_data),
    )
    created_project = Projects.get(Projects.title == mocked_data["title"])

    assert response.status_code == 201
    assert response.json == {"id": created_project.id}


def test_get_project_by_id_returning_status_200_and_json(client):
    random_id = uuid.uuid1()
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
    response = client.get(f"api/project/{id}", content_type="application/json")

    assert response.status_code == 200
    assert response.json == {"id": id, **dict_to_camel(mocked_data)}
