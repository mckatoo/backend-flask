def test_get_base_uri_status_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_base_uri_json_content_type(client):
    response = client.get("/")
    assert response.content_type == "application/json"


def test_get_base_uri_version_of_the_project(client):
    response = client.get("/")
    assert response.json == {"version": "1.0"}


def test_load_config(config):
    assert config["DEBUG"] is True
