from functools import wraps
from flask import request, jsonify
import jwt
from database.models.blacklist import Blacklist
from datetime import datetime, timezone
from configurations import envs_config


def decode_token(token: str) -> dict:
    return jwt.decode(token, envs_config.SECRET_KEY, algorithms="HS256")


def verify_token_middleware(func):
    @wraps(func)
    def decorated_func(*args, **kargs):
        try:
            token = str(request.headers["authentication"]).removeprefix(
                "Bearer "
            )
            decoded_token = decode_token(token)
            in_blacklist = bool(Blacklist.get_or_none(token=token))
            is_expired = (
                decoded_token["exp"] < datetime.now(tz=timezone.utc).timestamp()
            )

            if not in_blacklist and not is_expired:
                return func(*args, **kargs)
            return jsonify({"error": "Unauthorized"}), 401
        except Exception as e:
            if (
                str(e).__contains__("HTTP_AUTHENTICATION")
                or type(e) == jwt.DecodeError
            ):
                return jsonify(
                    {"error": "Unauthorized"},
                ), 401
            return jsonify({"error": "Unknown Error"}), 500

    return decorated_func
