import uuid

from database.models.images import Images
from database.models.pages import Pages


class RandomPageData:
    def __init__(self, image):
        random_id = uuid.uuid1()
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


def test_get_id_slug_and_status_201_on_create(client, image):
    data = RandomPageData(image)
    response = client.post(
        "api/page",
        json={
            "title": data.title,
            "description": data.description,
            "image": {"url": data.image.url, "alt": data.image.alt},
        },
    )
    page = Pages.get(Pages.title == data.title)
    assert response.status_code == 201
    assert response.json == {"id": page.id, "slug": page.slug}


def test_get_page_status_200_and_json_content_type(client, image):
    page, _ = create_image(image_data=image)
    response = client.get(f"api/page/{page.slug}")
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_get_page_content(client, image):
    page, image = create_image(image_data=image)
    response = client.get(f"api/page/{page.slug}")
    assert response.json == {
        "title": page.title,
        "description": page.description,
        "image": {
            "url": image.url,
            "alt": image.alt,
        },
    }


def test_get_status_204_on_update(client):
    response = client.patch("api/page/about-page")
    assert response.status_code == 204


def test_get_status_204_on_delete(client):
    response = client.patch("api/page/about-page")
    assert response.status_code == 204
