from flask import Blueprint, render_template, request, session, redirect, url_for
import requests

product_bp = Blueprint("product", __name__, template_folder="../templates")
BACKEND_URL = "http://127.0.0.1:5000"  # Base URL for API and images


def get_user_id():
    user = session.get("user")
    return user["id"] if user else None


def add_base_url_to_image(product):
    """If product has an image_url, prepend base URL."""
    if product and product.get("image_url"):
        # Ensure it doesn't already contain the full URL
        if not product["image_url"].startswith("http"):
            product["image_url"] = f"{BACKEND_URL}{product['image_url']}"
    return product


# List all products (optional filtering by category)
@product_bp.route("/", methods=["GET"])
def list_products():
    category = request.args.get("category")
    try:
        url = f"{BACKEND_URL}/products"
        if category:
            url += f"?category={category}"
        resp = requests.get(url)
        products = resp.json().get("data", [])

        # Add full URL for images
        for p in products:
            add_base_url_to_image(p)

    except Exception:
        products = []

    return render_template("products.html", products=products, category=category)


# View single product details
@product_bp.route("/<int:product_id>", methods=["GET"])
def view_product(product_id):
    try:
        resp = requests.get(f"{BACKEND_URL}/products/{product_id}")
        product = resp.json().get("data")
        if not product:
            return "Product not found", 404

        # Add full URL for image
        add_base_url_to_image(product)

    except Exception:
        product = None

    return render_template("product_detail.html", product=product)
