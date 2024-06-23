from flask import Blueprint, jsonify, request
from database.models.projects import Projects
from camel_converter import dict_to_camel
from playhouse.shortcuts import model_to_dict

projects_routes = Blueprint("projects_routes", __name__)
project_routes = Blueprint("project_routes", __name__)


#     re_path("^project/?$", CreateProject.as_view()),
@project_routes.route("", methods=["POST"])
def create_project():
    if not request.json:
        raise
    data = request.json
    project = Projects.create(
        title=data["title"],
        description=data["description"],
        snapshot=data["snapshot"],
        repository_link=data["repositoryLink"],
        start=data["start"],
        last_update=data["lastUpdate"],
    )
    return jsonify({"id": project.id}), 201


#  path("project/<int:pk>", GetUpdateDeleteProject.as_view()),
@project_routes.route("/<int:id>", methods=["GET"])
def get_project(id: int):
    project = Projects.get_by_id(id)
    return jsonify(dict_to_camel(model_to_dict(project))), 200


#     re_path("^projects/?$", ListProjects.as_view()),
