from peewee import CharField, Model
from database import db


class Blacklist(Model):
    class Meta:
        database = db
        table_name = "Blacklist"

    token = CharField(max_length=1000, null=False)
