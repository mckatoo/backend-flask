import json

def test_create_project_returning_status_201_and_id(client):
    mocked_request = json.dumps(
        {
            "from": "sender@mail.com",
            "to": "reciper@mail.com",
            "message": "hello",
        }
    )
    response = client.post(
        "api/project", content_type="application/json",
        data=mocked_request
    )

    assert response.status_code == 201
    assert response.json == {"id": 1}

def test_get_project_by_id_returning_status_200_and_json(client):
    response = client.get(
        "api/project/4", content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json == {"id": 4}