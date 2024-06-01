from flask import Blueprint, jsonify, request

from database.models.images import Images
from database.models.pages import Pages

page_routes = Blueprint("page_routes", __name__)


@page_routes.route("", methods=["POST"])
def create_page():
    if not request.json:
        raise
    data = request.json
    image = Images.create(url=data["image"]["url"], alt=data["image"]["alt"])
    page = Pages.create(
        title=data["title"],
        description=data["description"],
        image_id=image.id,
    )
    return jsonify({"id": page.id, "slug": page.slug}), 201


@page_routes.route("/<string:slug>", methods=["GET"])
def get_page(slug: str):
    page = Pages.get(Pages.slug == slug)
    image = Images.get_by_id(page.image_id)
    return jsonify(
        {
            "title": page.title,
            "description": page.description,
            "image": {
                "url": image.url,
                "alt": image.alt,
            },
        }
    ), 200


@page_routes.route("/<string:page>", methods=["PATCH"])
def update_page(page: str):
    return "", 204


@page_routes.route("/<string:page>", methods=["DELETE"])
def delete_page(page: str):
    return "", 204
