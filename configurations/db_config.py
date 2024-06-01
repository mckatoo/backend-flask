from database import db
from database.models.images import Images
from database.models.pages import Pages


def load_db_config():
    db.connect()
    db.create_tables([Pages, Images])
