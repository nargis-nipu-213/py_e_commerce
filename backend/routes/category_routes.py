from flask import Blueprint
from controllers.category_controller import list_categories, add_category, delete_category

category_bp = Blueprint("categories", __name__)
category_bp.route("/", methods=["GET"])(list_categories)
category_bp.route("/", methods=["POST"])(add_category)
category_bp.route("/<int:category_id>", methods=["DELETE"])(delete_category)
