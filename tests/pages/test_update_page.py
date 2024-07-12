from uuid import uuid1

from database.models.pages import Pages
from database.models.users import Users
from tests.utils import generate_mocked_user_data


def test_unauthorized_error_on_request_without_valid_token(client, image):
    response = client.patch(
        "api/page/about-page",
        headers={"authentication": "Bearer invalid-token"},
    )
    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_get_status_204_on_update(client):
    access_token = Users.create(
        **generate_mocked_user_data()
    ).generate_tokens()[0]

    random_id = uuid1()
    created_page = Pages.create(
        title=f"Title page {random_id}",
        description=f"Description page {random_id}",
        image_id=3,
    )
    new_data = {"description": f"Updated Description {uuid1()}"}

    response = client.patch(
        f"api/page/{created_page.slug}",
        json=new_data,
        headers={"authentication": f"Bearer {access_token}"},
    )
    updated_page = Pages.get_by_id(created_page.id)

    assert response.status_code == 204
    assert updated_page.description == new_data["description"]
