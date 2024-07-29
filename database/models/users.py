from datetime import datetime, timedelta, timezone

import jwt
from peewee import CharField, Model
from werkzeug.security import check_password_hash, generate_password_hash

from configurations.envs_config import SECRET_KEY
from database import db
from enum import Enum


class TokenType(Enum):
    ACCESS_TOKEN = "accessToken"
    REFRESH_TOKEN = "refreshToken"


class Users(Model):
    class Meta:
        database = db
        table_name = "Users"

    username = CharField(max_length=300, null=False, unique=True)
    email = CharField(max_length=300, null=False, unique=True)
    password = CharField(max_length=300, null=False)

    def save(self, *args, **kwargs):
        password = str(self.password) + str(SECRET_KEY)
        self.password = generate_password_hash(password)
        super(Users, self).save(*args, **kwargs)

    def verify_password(self, password):
        return check_password_hash(str(self.password), password + SECRET_KEY)

    def generate_token(self, type):
        expiration = 10 if type == TokenType.ACCESS_TOKEN else 60
        return jwt.encode(
            {
                "id": self.get_id(),
                "exp": datetime.now(tz=timezone.utc)
                + timedelta(
                    minutes=expiration
                ),
                "type": type.value,
            },
            SECRET_KEY,
        )

    def generate_refresh_token(self):
        return self.generate_token(type=TokenType.REFRESH_TOKEN)

    def generate_access_token(self):
        return self.generate_token(type=TokenType.ACCESS_TOKEN)

    def generate_tokens(self):
        id = self.get_id()
        if not id:
            raise Exception("Create user first.")
        access_token = self.generate_access_token()
        refresh_token = self.generate_refresh_token()
        user = {"username": self.username, "email": self.email}

        return dict(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user,
        )
