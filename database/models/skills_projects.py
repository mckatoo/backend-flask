from peewee import ForeignKeyField, Model

from database import db
from database.models.projects import Projects
from database.models.skills import Skills


class SkillsProjects(Model):
    class Meta:
        database = db
        table_name = "SkillsProjects"

    skill_id = ForeignKeyField(Skills, backref="skill")
    project_id = ForeignKeyField(Projects, backref="projects")
