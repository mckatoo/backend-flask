from flask import Blueprint, jsonify, request

from database.models.skills import Skills

skills_routes = Blueprint("skills_routes", __name__)
skill_routes = Blueprint("skill_routes", __name__)


@skill_routes.route("", methods=["POST"])
def create_skill():
    try:
        id = Skills.create(**request.json).get_id()
        return jsonify({"id": id}), 201
    except Exception as e:
        contain = str(e).lower().__contains__
        if contain("400") or contain("title"):
            return jsonify({"error": "Bad Request"}), 400
        return jsonify({"error": "Unknown Error"}), 500

# re_path("^skill/?$", CreateSkill.as_view()),
# re_path("^skill/<int:pk>/", GetUpdateDeleteSkill.as_view()),
# re_path("^skills/?$", ListSkills.as_view()),