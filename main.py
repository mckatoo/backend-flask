from flask import Flask

from app.routes import app_routes
from configurations.db_config import load_db_config
from configurations.envs import DEV_ENV
from pages.routes import page_routes
from images.routes import image_routes

app = Flask("web_app")

load_db_config()

app.register_blueprint(app_routes, url_prefix="/")
app.register_blueprint(page_routes, url_prefix="/api/page")
app.register_blueprint(image_routes, url_prefix="/api/image")

app.config["DEBUG"] = DEV_ENV
