from camel_converter import dict_to_camel
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

from database.models.projects import Projects
from database.models.skills import Skills
from database.models.skills_projects import SkillsProjects

skills_routes = Blueprint("skills_routes", __name__)
skill_routes = Blueprint("skill_routes", __name__)


@skill_routes.route("", methods=["POST"])
def create_skill():
    try:
        id = Skills.create(**request.json).get_id()
        return jsonify({"id": id}), 201
    except Exception as e:
        contain = str(e).lower().__contains__
        if contain("400") or contain("title"):
            return jsonify({"error": "Bad Request"}), 400
        return jsonify({"error": "Unknown Error"}), 500


@skill_routes.route("/<id>", methods=["GET"])
def get_skill_by_id(id):
    skill = Skills.get_by_id(id)
    skills_projects = list(
        SkillsProjects.select()
        .where(SkillsProjects.skill_id == skill.id)
        .dicts()
    )
    projects = [
        dict_to_camel(model_to_dict(Projects.get_by_id(skill_project["project_id"])))
        for skill_project in skills_projects
    ]

    return jsonify(
        {**dict_to_camel(model_to_dict(skill)), "projects": projects}
    ), 200


# re_path("^skill/<int:pk>/", GetUpdateDeleteSkill.as_view()),
# re_path("^skills/?$", ListSkills.as_view()),
