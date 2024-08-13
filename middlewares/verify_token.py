from functools import wraps
from flask import request, jsonify
import jwt
from database.models.blacklist import Blacklist
from datetime import datetime, timezone
from configurations import envs_config


def decode_token(token: str) -> dict:
    return jwt.decode(token, envs_config.SECRET_KEY, algorithms=["HS256"])


def verify_token_middleware(func):
    @wraps(func)
    def decorated_func(*args, **kargs):
        if "authorization" not in request.headers:
            return jsonify({"error": "Unauthorized"}), 401
        try:
            token = str(request.headers["authorization"]).removeprefix(
                "Bearer "
            )
            decoded_token = decode_token(token)
            in_blacklist = bool(Blacklist.get_or_none(token=token))
            is_expired = bool(
                decoded_token["exp"] < datetime.now(tz=timezone.utc).timestamp()
            )

            if in_blacklist or is_expired:
                return jsonify({"error": "Unauthorized"}), 401
            return func(*args, **kargs)
        except Exception as e:
            if (
                str(e).__contains__("HTTP_AUTHENTICATION")
                or type(e) == jwt.DecodeError
                or type(e) == jwt.ExpiredSignatureError
            ):
                return jsonify(
                    {"error": "Unauthorized"},
                ), 401

            if(type(e) == KeyError):
                return jsonify(
                    {"error": "Bad Request"},
                ), 400
                
            return jsonify({"error": "Unknown Error"}), 500

    return decorated_func
