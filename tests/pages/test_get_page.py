from tests.pages.test_create_page import create_image


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
