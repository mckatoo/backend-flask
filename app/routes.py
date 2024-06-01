from flask import Blueprint, jsonify

app_routes = Blueprint("root", __name__)


@app_routes.route("/", methods=["GET"])
def index():
    return jsonify({"version": "1.0"}), 200
