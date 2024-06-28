from flask import Flask

from app.routes import app_routes
from authentication.routes import auth_routes
from configurations.db_config import load_db_config
from configurations.envs_config import DEV_ENV
from images.routes import image_routes
from mailer.routes import mailer_routes
from pages.routes import page_routes
from projects.routes import project_routes, projects_routes
from skills.routes import skill_routes, skills_routes

app = Flask("web_app")

load_db_config()

app.register_blueprint(app_routes, url_prefix="/")
app.register_blueprint(page_routes, url_prefix="/api/page")
app.register_blueprint(image_routes, url_prefix="/api/image")
app.register_blueprint(mailer_routes, url_prefix="/api/mailer")
app.register_blueprint(projects_routes, url_prefix="/api/projects")
app.register_blueprint(project_routes, url_prefix="/api/project")
app.register_blueprint(skills_routes, url_prefix="/api/skills")
app.register_blueprint(skill_routes, url_prefix="/api/skill")
app.register_blueprint(auth_routes, url_prefix="/api/auth")

app.config["DEBUG"] = DEV_ENV
