from database.models.users import Users
from tests.utils import generate_mocked_user_data


def test_unauthorized_error_on_request_without_valid_token(client):
    response = client.delete(
        "api/user/token",
        headers={"authentication": "Bearer invalid-token"},
        content_type="application/json",
    )
    
    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}

def test_delete_user_and_return_204_status_code(client):
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()

    response = client.delete(
        f"api/user/{existent_user.id}",
        headers={"authentication": f"Bearer {access_token}"},
        content_type="application/json",
    )
    deleted_user = Users.get_or_none(Users.id == existent_user.id)

    assert response.status_code == 204
    assert deleted_user is None


def test_error_400_when_request_delete_without_id(client):
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()
    response = client.delete(
        "api/user",
        headers={"authentication": f"Bearer {access_token}"},
        content_type="application/json",
    )
    
    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}


def test_error_400_when_request_delete_with_invalid_id(client):
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()
    response = client.delete(
        "api/user/invalid-id",
        headers={"authentication": f"Bearer {access_token}"},
        content_type="application/json",
    )
    
    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}
