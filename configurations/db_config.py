from database import db
from database.models.blacklist import Blacklist
from database.models.images import Images
from database.models.pages import Pages
from database.models.projects import Projects
from database.models.skills import Skills
from database.models.skills_projects import SkillsProjects
from database.models.users import Users


def load_db_config():
    db.connect()
    db.create_tables(
        [Pages, Images, Projects, Skills, SkillsProjects, Users, Blacklist]
    )
