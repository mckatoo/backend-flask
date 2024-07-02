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
        self.password = generate_password_hash(str(self.password))
        super(Users, self).save(*args, **kwargs)

    def verify_password(self, password):
        return check_password_hash(str(self.password), password)

    def generate_tokens(self):
        if not self.id:
            raise Exception("Create user first.")
        access_token = jwt.encode(
            {
                "id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
            },
            envs_config.SECRET_KEY,
        )
        refresh_token = jwt.encode(
            {
                "id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
            },
            envs_config.SECRET_KEY,
        )

        return access_token, refresh_token
