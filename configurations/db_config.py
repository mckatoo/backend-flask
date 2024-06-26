from database import db
from database.models.images import Images
from database.models.pages import Pages
from database.models.projects import Projects
from database.models.skills import Skills
from database.models.skills_projects import SkillsProjects


def load_db_config():
    db.connect()
    db.create_tables([Pages, Images, Projects, Skills, SkillsProjects])
