from uuid import uuid1
import pytest
from main import app as web_app


@pytest.fixture()
def app():
    web_app.config.update(
        {
            "TESTING": True,
        }
    )

    yield web_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def image():
    class RandomImageData:
        def __init__(self):
            random_id = uuid1()
            self.url = f"{random_id} url of page image"
            self.alt = f"{random_id} Description of page image"

    return RandomImageData()
