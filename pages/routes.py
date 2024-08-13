from flask import Blueprint, jsonify, request

from database.models.images import Images
from database.models.pages import Pages
from middlewares.verify_token import verify_token_middleware

page_routes = Blueprint("page_routes", __name__)


@page_routes.route("", methods=["POST"])
@verify_token_middleware
def create_page():
    if not request.json:
        raise
    data = request.json
    page = Pages()
    page.title = data["title"]
    page.description = data["description"]
    if "image" in data and "url" in data["image"] and "alt" in data["image"]:
        image = Images.create(
            url=data["image"]["url"], alt=data["image"]["alt"]
        )
        page.image_id = image.id
    page.save()
    return jsonify({"id": page.id, "slug": page.slug}), 201


@page_routes.route("/<string:slug>", methods=["GET"])
def get_page(slug: str):
    try:
        page = Pages.get(Pages.slug == slug)
        data = {"title": page.title, "description": page.description}
        if page.image_id:
            image = Images.get_by_id(page.image_id)
            data["image"] = {
                "url": image.url,
                "alt": image.alt,
            }
        return jsonify(data), 200
    except Exception:
        return {"error": "Unknown Error"}, 500


@page_routes.route("/<string:slug>", methods=["PATCH"])
@verify_token_middleware
def update_page(slug: str):
    try:
        Pages.update(**request.json).where(Pages.slug == slug).execute()
        return jsonify({}), 204
    except Exception as e:
        contain = str(e).lower().__contains__
        if contain("400") or contain("415"):
            return jsonify({"error": "Bad Request"}), 400
        if contain("not") and contain("found"):
            return jsonify({"error": "Not Found"}), 404
        return jsonify({"error": "Unkown Error"}), 500


@page_routes.route("/<string:slug>", methods=["DELETE"])
@verify_token_middleware
def delete_page(slug: str):
    try:
        Pages.delete().where(Pages.slug == slug).execute()
        return jsonify({}), 204
    except Exception as e:
        contain = str(e).lower().__contains__
        if contain("400") or contain("415"):
            return jsonify({"error": "Bad Request"}), 400
        if contain("not") and contain("found"):
            return jsonify({"error": "Not Found"}), 404
        return jsonify({"error": "Unkown Error"}), 500
