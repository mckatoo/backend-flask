from flask import Blueprint, jsonify, request

from configurations.cloudinary_config import (
    destroy,
    get_resource,
    image_uploader,
)
from configurations.envs_config import IMAGE_ALLOWED_EXTENSIONS
from middlewares.verify_token import verify_token_middleware

image_routes = Blueprint("image_routes", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS
    )


@image_routes.route("", methods=["GET"])
def get_image():
    try:
        public_id: str = request.json["id"]
        result = get_resource(public_id)
        return jsonify({"url": result["url"]}), 200
    except Exception as e:
        if str(e).__contains__("404"):
            return jsonify({"error": "Image not found"}), 404
        if str(e).__contains__("400"):
            return jsonify({"error": "No id"}), 400
        return jsonify({"error": "Unexpected error"}), 500


@image_routes.route("", methods=["POST"])
@verify_token_middleware
def send_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    if not file or file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and not allowed_file(file.filename):
        return jsonify({"error": "Not allowed file"}), 400

    response = image_uploader(file)
    public_id = response["public_id"]
    secure_url = response["secure_url"]

    return jsonify(
        {
            "url": secure_url,
            "publicId": public_id,
        }
    ), 201


@image_routes.route("", methods=["DELETE"])
@verify_token_middleware
def delete_image():
    try:
        if not request.json or "id" not in request.json:
            raise "400"
        public_id: str = request.json["id"]
        destroy(public_id)
        return "", 204
    except Exception as e:
        if str(e).__contains__("400"):
            return jsonify({"error": "No id"}), 400
        return jsonify({"error": "Unexpected error"}), 500
