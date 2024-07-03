from database.models.users import Users
from tests.utils import generate_mocked_user_data, remove_id
from playhouse.shortcuts import model_to_dict


def test_get_user_by_id(client):
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()

    response = client.get(f"api/user/{existent_user.id}")

    assert response.status_code == 200
    assert response.json == model_to_dict(existent_user)

def test_error_400_when_request_user_without_id(client):
    response = client.get("api/user")

    assert response.status_code == 400
    assert response.json == {"error": "Bad Request"}

def test_error_404_when_not_found_user(client):
    response = client.get("api/user/invalid-user-id")

    assert response.status_code == 404
    assert response.json == {"error": "Not Found"}

def test_list_all_users(client):
    Users.delete().execute()
    mock_users = [generate_mocked_user_data() for _ in range(5)]
    Users.bulk_create([Users(**user) for user in mock_users])
    
    response = client.get("api/users")
    response_without_id = list(map(remove_id, response.json))

    assert response.status_code == 200
    assert response_without_id == mock_users

def test_return_empty_list_when_not_found_users(client):
    Users.delete().execute()
    response = client.get("api/users")

    assert response.status_code == 200
    assert response.json == []