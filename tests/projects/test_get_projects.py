import uuid

from camel_converter import dict_to_camel
from playhouse.shortcuts import dict_to_model, model_to_dict

from database.models.projects import Projects
from tests.utils import remove_id


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


def test_error_when_request_project_with_id_not_found(client):
    response = client.get(
        "api/project/not-found-id", content_type="application/json"
    )

    assert response.status_code == 404
    assert response.json == {"error": "Not Found"}


def test_error_when_request_project_without_id(client):
    response = client.get("api/project", content_type="application/json")

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}


def test_list_all_projects(client):
    Projects.delete().execute()
    projects_list = [
        Projects(
            title=f"Title test {i}",
            description=f"Description test  {i}",
            snapshot=f"http://snapshot.com/image-{i}.jpg",
            repository_link=f"http://repository.com/my{i}.git",
            start="2024/03/22",
            last_update="2024/06/13",
        )
        for i in range(5)
    ]
    Projects.bulk_create(projects_list)
    projects_list = list(map(model_to_dict, projects_list))
    response = client.get("api/projects", content_type="application/json")

    response_list = list(map(remove_id, response.json))
    projects_list = list(map(remove_id, projects_list))

    assert response.status_code == 200
    assert response_list == projects_list


def test_empty_list_when_no_product(client):
    Projects.delete().execute()
    response = client.get("api/projects", content_type="application/json")

    assert response.status_code == 200
    assert response.json == []
