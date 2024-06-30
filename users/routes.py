from camel_converter import dict_to_camel, dict_to_snake
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

from database.models.users import Users
from middlewares.verify_token import verify_token_middleware

users_routes = Blueprint("users_routes", __name__)
user_routes = Blueprint("user_routes", __name__)


@user_routes.route("", methods=["POST"])
@verify_token_middleware
def create_user():
    return jsonify({}), 201