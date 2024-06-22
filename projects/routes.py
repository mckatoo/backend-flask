
from flask import Blueprint, jsonify, request

projects_routes = Blueprint("projects_routes", __name__)
project_routes = Blueprint("project_routes", __name__)


#  path("project/<int:pk>", GetUpdateDeleteProject.as_view()),
@project_routes.route("/<int:id>", methods=["GET"])
def get_project(id: int):
    return jsonify({"id": id}),200


#     re_path("^project/?$", CreateProject.as_view()),
@project_routes.route("", methods=["POST"])
def create_project():
    return jsonify({"id": 1}),201
#     re_path("^projects/?$", ListProjects.as_view()),