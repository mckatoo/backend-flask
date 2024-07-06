def test_unauthorized_error_on_request_without_valid_token(client, image):
    response = client.patch(
        "api/page/about-page",
        headers={"authentication": "Bearer invalid-token"},
    )
    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}


def test_get_status_204_on_delete(client):
    response = client.patch("api/page/about-page")
    assert response.status_code == 204
