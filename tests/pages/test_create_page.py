from uuid import uuid4

from database.models.images import Images
from database.models.pages import Pages
from database.models.users import Users
from tests.utils import generate_mocked_user_data


class RandomPageData:
    def __init__(self, image):
        random_id = uuid4()
        self.title = f"{random_id} tile of page"
        self.description = f"{random_id} description of page"
        self.image = image


def create_image(image_data):
    expected = RandomPageData(image=image_data)
    new_image = Images.create(url=expected.image.url, alt=expected.image.alt)
    page = Pages.create(
        title=expected.title,
        description=expected.title,
        image_id=new_image.id,
    )
    return page, new_image


def test_unauthorized_error_on_request_without_valid_token(client, image):
    data = RandomPageData(image)
    response = client.post(
        "api/page",
        headers={"authorization": "Bearer invalid-token"},
        json={
            "title": data.title,
            "description": data.description,
            "image": {"url": data.image.url, "alt": data.image.alt},
        },
    )
    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_create_page(client, image):
    access_token = Users.create(
        **generate_mocked_user_data()
    ).generate_tokens()["access_token"]
    data = RandomPageData(image)
    response = client.post(
        "api/page",
        json={
            "title": data.title,
            "description": data.description,
            "image": {"url": data.image.url, "alt": data.image.alt},
        },
        headers={"authorization": f"Bearer {access_token}"},
    )
    page = Pages.get(Pages.title == data.title)
    assert response.status_code == 201
    assert response.json == {"id": page.id, "slug": page.slug}

def test_create_page_with_slug(client, image):
    access_token = Users.create(
        **generate_mocked_user_data()
    ).generate_tokens()["access_token"]
    data = RandomPageData(image)
    data.slug = f"{uuid4()}-page"
    response = client.post(
        "api/page",
        json={
            "title": data.title,
            "slug": data.slug,
            "description": data.description,
            "image": {"url": data.image.url, "alt": data.image.alt},
        },
        headers={"authorization": f"Bearer {access_token}"},
    )
    page = Pages.get(Pages.title == data.title)
    assert response.status_code == 201
    assert response.json == {"id": page.id, "slug": data.slug}
