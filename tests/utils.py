from random import randint
from uuid import uuid4


def remove_id(dictionary):
    dictionary.pop("id")
    return dictionary


def generate_mocked_user_data():
    random_id = randint(1, 1000)

    return {
        "username": f"user_{random_id}",
        "email": f"{random_id}@email.com",
        "password": f"pass_{uuid4()}",
    }
