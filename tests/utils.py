from uuid import uuid1


def remove_id(dictionary):
    dictionary.pop("id")
    return dictionary


def generate_mocked_user_data():
    random_id = uuid1()
    return {
        "username": f"user_{random_id}",
        "email": f"{random_id}@email.com",
        "password": f"pass_{random_id}",
    }
