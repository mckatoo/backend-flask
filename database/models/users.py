from datetime import datetime, timedelta, timezone

import jwt
from peewee import CharField, Model
from werkzeug.security import check_password_hash, generate_password_hash

from configurations import envs_config
from database import db


class Users(Model):
    class Meta:
        database = db
        table_name = "Users"

    username = CharField(max_length=300, null=False, unique=True)
    email = CharField(max_length=300, null=False, unique=True)
    password = CharField(max_length=300, null=False)

    def save(self, *args, **kwargs):
        password = str(self.password) + str(envs_config.SECRET_KEY)
        self.password = generate_password_hash(password)
        super(Users, self).save(*args, **kwargs)

    def verify_password(self, password):
        return check_password_hash(
            str(self.password), password + envs_config.SECRET_KEY
        )

    def generate_tokens(self):
        id = self.get_id()
        if not id:
            raise Exception("Create user first.")
        access_token = jwt.encode(
            {
                "id": id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
            },
            envs_config.SECRET_KEY,
        )
        refresh_token = jwt.encode(
            {
                "id": id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=60),
            },
            envs_config.SECRET_KEY,
        )
        user = {"username": self.username, "email": self.email}

        return access_token, refresh_token, user
