from flask import Blueprint, jsonify, request

from configurations.envs import IMAGE_ALLOWED_EXTENSIONS

image_routes = Blueprint("image_routes", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS
    )


@image_routes.route("", methods=["GET"])
def get_image():
    return jsonify({"url": "url"}), 200


@image_routes.route("", methods=["POST"])
def send_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and not allowed_file(file.filename):
        return jsonify({"error": "Not allowed file"})

    # cloudinary implementation

    return jsonify(
        {
            "url": "secure_url",
            "publicId": "public_id",
        }
    ), 201


@image_routes.route("", methods=["DELETE"])
def delete_image():
    return "", 204
