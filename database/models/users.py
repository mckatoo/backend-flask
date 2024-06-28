from peewee import CharField, Model
from werkzeug.security import check_password_hash, generate_password_hash

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
