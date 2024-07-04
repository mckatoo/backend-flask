import secrets

from flask import Blueprint, jsonify, request
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict

from configurations.envs_config import SMTP_USERNAME
from configurations.mail_config import send_mail
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


@user_routes.route("/<id>", methods=["DELETE"])
@verify_token_middleware
def delete_user(id):
    try:
        user = Users.get_by_id(id)
        user.delete_instance()
        return jsonify({}), 204
    except Exception as e:
        contains = str(e).lower().__contains__
        if contains("not") and contains("exist"):
            return jsonify({"error": "Bad Request"}), 400
        return jsonify({"error": "Unknown Error"}), 500


@user_routes.route("/<id>", methods=["PATCH"])
@verify_token_middleware
def update_user(id):
    try:
        data = request.json
        Users.update(**data).where(Users.id == id).execute()
        return jsonify({}), 204
    except Exception as e:
        contain = str(e).lower().__contains__
        if contain("400"):
            return jsonify({"error": "Bad Request"}), 400
        if contain("not") and contain("found"):
            return jsonify({"error": "Not Found"}), 404
        return jsonify({"error": "Unkown Error"}), 500


@user_routes.route("/recovery-password", methods=["POST"])
def recovery_password():
    try:
        email = request.json["email"]
        user = Users.get(Users.email == email)
        password_length = 13
        new_password = secrets.token_urlsafe(password_length)
        user.password = new_password
        user.save()
        message: str = f"Your new password is: {new_password}"
        subject: str = "Recovery password."
        send_mail(
            sender=SMTP_USERNAME,
            recipients=email,
            message=message,
            subject=subject,
        )
        return jsonify({"message": "Success"}), 204
    except Exception as e:
        contain = str(e).lower().__contains__
        if contain("400"):
            return jsonify({"error": "Bad Request"}), 400
        if contain("not") and contain("exist"):
            return jsonify({"error": "Not Found"}), 404
        return jsonify({"error": "Unkown Error"}), 500
