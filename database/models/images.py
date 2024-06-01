from peewee import CharField, Model
from database import db


class Images(Model):
    class Meta:
        database = db
        table_name = "Images"

    url = CharField(max_length=300, null=False)
    alt = CharField(max_length=300, null=False)
