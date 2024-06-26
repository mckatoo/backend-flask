from datetime import datetime

from peewee import CharField, DateField, Model, TextField

from database import db


class Projects(Model):
    class Meta:
        database = db
        table_name = "Projects"

    title = CharField(max_length=200, null=False, unique=True)
    description = TextField(null=False)
    snapshot = CharField(max_length=200, null=False)
    repository_link = CharField(null=False)
    start = DateField(default=datetime.now().date())
    last_update = DateField(default=datetime.now().date())
