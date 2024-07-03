from database.models.users import Users
from tests.utils import generate_mocked_user_data


def test_delete_user_and_return_204_status_code(client):
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()

    response = client.delete(f"api/user/{existent_user.id}")
    deleted_user = Users.get_or_none(Users.id == existent_user.id)

    assert response.status_code == 204
    assert deleted_user is None


def test_error_400_when_request_delete_without_data(client):
    assert False


def test_error_400_when_request_delete_with_invalid_data(client):
    assert False
