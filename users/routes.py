from flask import Blueprint, jsonify, request
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict

from database.models.users import Users
from middlewares.verify_token import verify_token_middleware

users_routes = Blueprint("users_routes", __name__)
user_routes = Blueprint("user_routes", __name__)


@user_routes.route("", methods=["POST"])
@verify_token_middleware
def create_user():
    try:
        created_user = Users.create(**request.json)
        return jsonify({"id": created_user.id}), 201
    except Exception as e:
        if str(e).lower().__contains__("400") or type(e) == IntegrityError:
            return jsonify({"error": "Bad Request"}), 400
        return jsonify({"error": "Unexpected Error"}), 500


@user_routes.route("", methods=["GET", "PATCH", "DELETE"])
def bad_request():
    return jsonify({"error": "Bad Request"}), 400


@user_routes.route("/<id>", methods=["GET"])
def get_user_by_id(id):
    try:
        user = Users.get_by_id(id)
        return jsonify(model_to_dict(user)), 200
    except Exception as e:
        contains = str(e).lower().__contains__
        if contains("400"):
            return jsonify({"error": "Bad Request"}), 400
        if contains("not") and contains("exist"):
            return jsonify({"error": "Not Found"}), 404
        return jsonify({"error": "Unknown Error"}), 500

@users_routes.route("", methods=["GET"])
def list_users():
    users = list(Users.select().dicts())
    return jsonify(users), 200
