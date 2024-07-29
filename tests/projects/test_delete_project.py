from uuid import uuid1

from playhouse.shortcuts import dict_to_model

from database.models.projects import Projects
from database.models.users import Users
from tests.utils import generate_mocked_user_data

access_token = Users.create(**generate_mocked_user_data()).generate_tokens()["access_token"]


def test_unauthorized_error_on_request_without_valid_token(client):
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
        f"api/project/{id}",
        headers={"authentication": "Bearer invalid-token"},
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


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
        f"api/project/{id}",
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 204
    assert not Projects.get_or_none(Projects.id == id)


def test_error_when_request_without_id(client):
    response = client.delete(
        "api/project",
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
