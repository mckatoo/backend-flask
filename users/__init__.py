from database.models.users import Users
from tests.utils import generate_mocked_user_data


def make_init_user():
    if not Users.get_or_none():
        user = generate_mocked_user_data()
        print("INITIAL USER")
        print(user.__str__())
        Users.create(**user)
