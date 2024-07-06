from peewee import CharField, ForeignKeyField, Model, TextField
from database import db
from flask_peewee.utils import slugify

from database.models.images import Images


class Pages(Model):
    class Meta:
        database = db
        table_name = "Pages"

    title = CharField(null=False, max_length=200)
    description = TextField(null=False)
    slug = CharField(
        max_length=250,
        null=True,
        unique=True,
        default=""
    )
    image_id = ForeignKeyField(Images, backref="image", null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Pages, self).save(*args, **kwargs)
