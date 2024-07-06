from camel_converter import dict_to_camel, dict_to_snake
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

from database.models.projects import Projects
from middlewares.verify_token import verify_token_middleware

projects_routes = Blueprint("projects_routes", __name__)
project_routes = Blueprint("project_routes", __name__)


@project_routes.route("", methods=["POST"])
@verify_token_middleware
def create_project():
    try:
        if not request.json:
            raise Exception("400")
        project = Projects.create(**dict_to_snake(request.json))
        return jsonify({"id": project.id}), 201
    except Exception as e:
        if str(e).__contains__("400"):
            return jsonify({"error": "Bad Request"}), 400
        return jsonify({"error": "Unknown Error"}), 500


@project_routes.route("", methods=["GET", "PATCH", "DELETE"])
def without_id():
    return jsonify({"error": "Bad Request"}), 400


@project_routes.route("/<id>", methods=["GET"])
def get_project(id):
    try:
        project = Projects.get_by_id(id)
        return jsonify(dict_to_camel(model_to_dict(project))), 200
    except Exception as e:
        contain = str(e).lower().__contains__
        if contain("not") and contain("found"):
            return jsonify({"error": "Not Found"}), 404
        if contain("400"):
            return jsonify({"error": "Bad Request"}), 400
        return jsonify({"error": "Unkown Error"}), 500


@projects_routes.route("", methods=["GET"])
def list_projects():
    try:
        projects = list(Projects.select().dicts())
        return jsonify(projects), 200
    except Exception as e:
        contain = str(e).lower().__contains__
        if contain("not") and contain("found"):
            return jsonify({"error": "Not Found"}), 404
        return jsonify({"error": "Unknown Error"}), 500


@project_routes.route("/<id>", methods=["PATCH"])
@verify_token_middleware
def update_project(id):
    try:
        Projects.update(**request.json).where(Projects.id == id).execute()
        return jsonify({}), 204
    except Exception as e:
        contain = str(e).lower().__contains__
        if contain("400"):
            return jsonify({"error": "Bad Request"}), 400
        if contain("not") and contain("found"):
            return jsonify({"error": "Not Found"}), 404
        return jsonify({"error": "Unkown Error"}), 500


@project_routes.route("/<id>", methods=["DELETE"])
@verify_token_middleware
def delete_project(id):
    try:
        Projects.delete_by_id(id)
        return jsonify({}), 204
    except Exception as e:
        if str(e).lower().__contains__("400"):
            return jsonify({"error": "Bad Request"}), 400
        return jsonify({"error": "Unknown Error"}), 500
