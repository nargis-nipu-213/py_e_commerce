from flask import request, jsonify
from middlewares.admin_required import admin_required
from services.category_service import CategoryService

category_service = CategoryService()

def response_success(data=None, message="Success"):
    return jsonify({"message": message, "data": data if data is not None else {}})

def response_error(message="Error", status_code=400):
    return jsonify({"message": message, "data": {}}), status_code

def list_categories():
    categories = category_service.list()
    return response_success(categories, "Categories retrieved")

@admin_required
def add_category():
    data = request.json
    if not data.get("name"):
        return response_error("Category name is required")

    category = category_service.add(data["name"])
    if not category:
        return response_error("Category already exists")

    return response_success(category, "Category added")


@admin_required
def delete_category(category_id):
    category_service.delete(category_id)
    return response_success({}, "Category deleted")
