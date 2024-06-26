from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, jsonify, request

from configurations import envs_config
from database.models.users import Users
from database.models.blacklist import Blacklist

auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.route("/sign-in", methods=["POST"])
def sign_in():
    try:
        if not request.json:
            raise Exception("400")
        email = request.json["email"]
        password = request.json["password"]
        user = Users.get_or_none(email=email)
        if not user or not user.verify_password(password):
            raise
        access_token = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
            },
            envs_config.SECRET_KEY,
        )
        refresh_token = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=60),
            },
            envs_config.SECRET_KEY,
        )

        return jsonify(
            {"accessToken": access_token, "refreshToken": refresh_token}
        )
    except Exception as e:
        if str(e).__contains__("400"):
            return jsonify({"error": "Bad Request"}), 400
        return jsonify({"error": "Unauthorized"}), 401


@auth_routes.route("/sign-out", methods=["POST"])
def sign_out():
    access_token = str(request.headers["authentication"]).removeprefix(
        "Bearer "
    )
    Blacklist.create(token=access_token)

    return jsonify({}), 200


# re_path("^verify-token/?$", verify), GET
# re_path("^refresh/?$", verify),


# @api_view(["POST"])
# def sign_out(_):
#     return Response()


# @api_view(["GET"])
# def verify(_):
#     return Response()


# @api_view(["POST"])
# def refresh(_):
#     return Response()
