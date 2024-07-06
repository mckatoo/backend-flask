import json
import uuid

from camel_converter import dict_to_snake
from playhouse.shortcuts import model_to_dict

from database.models.projects import Projects
from database.models.users import Users
from tests.utils import generate_mocked_user_data

access_token, _ = Users.create(**generate_mocked_user_data()).generate_tokens()


def test_unauthorized_error_on_request_without_valid_token(client):
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
        headers={"authentication": "Bearer invalid-token"},
        content_type="application/json",
        data=json.dumps(mocked_data),
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


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
        headers={"authentication": f"Bearer {access_token}"},
    )
    created_project = Projects.get(Projects.title == mocked_data["title"])

    assert response.status_code == 201
    assert response.json == {"id": created_project.id}
    assert model_to_dict(created_project) == {
        "id": created_project.id,
        **dict_to_snake(mocked_data),
    }


def test_error_when_try_create_projects_without_data(client):
    response = client.post(
        "api/project",
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}


def test_error_when_try_create_projects_wit_invalid_data(client):
    response = client.post(
        "api/project",
        data={"invalid": "data"},
        content_type="application/json",
        headers={"authentication": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
