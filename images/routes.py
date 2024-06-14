from flask import Blueprint, jsonify, request

from configurations.cloudinary_config import (
    destroy,
    image_uploader,
    get_resource,
)
from configurations.envs_config import IMAGE_ALLOWED_EXTENSIONS

image_routes = Blueprint("image_routes", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS
    )


@image_routes.route("", methods=["GET"])
def get_image():
    if request.json and "id" in request.json:
        public_id: str = request.json["id"]
        result = get_resource(public_id)
        return jsonify({"url": result["url"]}), 200

    return jsonify({"error": "No id"}), 400


@image_routes.route("", methods=["POST"])
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
def delete_image():
    print("request.json ===>", request.json)
    if request.json and "id" in request.json:
        public_id: str = request.json["id"]
        destroy(public_id)
        return "", 204

    return jsonify({"error": "No id"}), 400
