from database.models.users import Users
from tests.utils import generate_mocked_user_data
import json
from playhouse.shortcuts import model_to_dict
from uuid import uuid1

def test_unauthorized_error_on_request_without_valid_token(client):
    response = client.patch(
        "api/user/token",
        headers={"authentication": "Bearer invalid-token"},
        content_type="application/json",
    )
    
    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}

def test_update_user_and_return_204_status_code(client):
    random_id = uuid1()
    mocked_new_data = {"email": f"updated_{random_id}@email.com"},
    existent_user_data = generate_mocked_user_data()
    existent_user = Users.create(**existent_user_data)
    access_token, _ = existent_user.generate_tokens()
    id = existent_user.id
    response = client.patch(
        f"api/user/{id}",
        headers={"authentication": f"Bearer {access_token}"},
        data=json.dumps(mocked_new_data),
        content_type="application/json",
    )
    updated_user = model_to_dict(Users.get_by_id(id))
    
    assert response.status_code == 204
    assert updated_user == {"id": id, **existent_user_data, **mocked_new_data}

def test_error_400_when_request_update_without_data(client):
    assert False

def test_error_400_when_request_update_with_invalid_data(client):
    assert False