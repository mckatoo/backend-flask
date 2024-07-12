from database.models.users import Users
from database.models.pages import Pages
from tests.utils import generate_mocked_user_data
from uuid import uuid1

access_token = Users.create(**generate_mocked_user_data()).generate_tokens()[0]


def test_unauthorized_error_on_request_without_valid_token(client, image):
    response = client.patch(
        "api/page/about-page",
        headers={"authentication": "Bearer invalid-token"},
    )
    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_get_status_204_on_delete(client):
    random_id = uuid1()
    created_page = Pages.create(
        title=f"Title page {random_id}",
        description=f"Description page {random_id}",
    )
    response = client.delete(
        f"api/page/{created_page.slug}",
        headers={"authentication": f"Bearer {access_token}"},
    )
    deleted_page = Pages.get_or_none(Pages.id == created_page.id)

    assert response.status_code == 204
    assert deleted_page is None
