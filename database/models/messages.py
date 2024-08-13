from peewee import TextField, CharField, Model

from database import db


class Messages(Model):
    class Meta:
        database = db
        table_name = "Messages"

    sender = CharField(max_length=300, null=False)
    recipients = CharField(max_length=300, null=False)
    subject = CharField(max_length=300, null=False)
    message = TextField(null=False)
