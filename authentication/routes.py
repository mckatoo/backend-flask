from flask import Blueprint, jsonify, request

from database.models.blacklist import Blacklist
from database.models.users import Users
from middlewares.verify_token import decode_token, verify_token_middleware

auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.route("/sign-in", methods=["POST"])
def sign_in():
    try:
        if not request.json:
            raise Exception("400")

        password = request.json["password"]

        if "username" in request.json:
            user = Users.get_or_none(Users.username == request.json["username"])
        else:
            user = Users.get_or_none(Users.email == request.json["email"])

        if not user or not user.verify_password(password):
            raise
        access_token, refresh_token, user = user.generate_tokens()

        return jsonify(
            {
                "accessToken": access_token,
                "refreshToken": refresh_token,
                "user": user,
            }
        )
    except Exception as e:
        if str(e).__contains__("400"):
            return jsonify({"error": "Bad Request"}), 400
        return jsonify({"error": "Unauthorized"}), 401


@auth_routes.route("/sign-out", methods=["POST"])
@verify_token_middleware
def sign_out():
    access_token = str(request.headers["authentication"]).removeprefix(
        "Bearer "
    )
    Blacklist.create(token=access_token)

    return jsonify({}), 200


@auth_routes.route("/verify-token", methods=["POST"])
@verify_token_middleware
def verify_token():
    try:
        access_token = str(request.headers["authentication"]).removeprefix(
            "Bearer "
        )
        decoded_token = decode_token(access_token)
        user = Users.get_by_id(decoded_token["id"])

        return jsonify({"username": user.username, "email": user.email}), 200
    except Exception as e:
        contain = str(e).lower().__contains__
        if contain("not") and contain("exist"):
            return jsonify({"error": "Unauthorized"}), 401
        return jsonify({"error": e}), 500


# re_path("^refresh/?$", verify),

# @api_view(["POST"])
# def refresh(_):
#     return Response()
