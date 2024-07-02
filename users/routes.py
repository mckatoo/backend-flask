from flask import Blueprint, jsonify, request

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
        return jsonify({"error": "Unexpected Error"}), 500
