from peewee import CharField, Model

from database import db


class Skills(Model):
    class Meta:
        database = db
        table_name = "Skills"

    title = CharField(max_length=200, null=False, unique=True)
