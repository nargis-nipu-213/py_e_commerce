from flask import Blueprint, render_template, request, session, redirect, url_for
import requests

BACKEND_URL = "http://127.0.0.1:5000"
product_bp = Blueprint("product", __name__, template_folder="../templates")


def get_admin_headers():
    admin = session.get("admin")
    if not admin:
        return None
    return {"X-ADMIN-ID": str(admin["id"])}


@product_bp.route("/", methods=["GET"])
def list_products():
    headers = get_admin_headers()
    if not headers:
        return redirect(url_for("auth.login"))
    try:
        resp = requests.get(f"{BACKEND_URL}/products/", headers=headers)
        products = resp.json().get("data", [])
    except Exception:
        products = []
    return render_template("admin_products.html", products=products)


@product_bp.route("/add", methods=["GET", "POST"])
def add_product():
    headers = get_admin_headers()
    if not headers:
        return redirect(url_for("auth.login"))

    # Fetch categories for dropdown
    try:
        cat_resp = requests.get(f"{BACKEND_URL}/categories/", headers=headers)
        categories = cat_resp.json().get("data", [])
    except Exception:
        categories = []

    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        category_id = request.form.get("category_id")
        description = request.form.get("description")
        image_file = request.files.get("image_file")

        image_url = None

        # ✅ IMAGE UPLOAD (FIXED)
        if image_file and image_file.filename:
            files = {
                "image": (
                    image_file.filename,                 # real filename
                    image_file.stream,                   # file stream
                    image_file.mimetype or "application/octet-stream",
                )
            }

            try:
                img_resp = requests.post(
                    f"{BACKEND_URL}/images/upload",
                    files=files,
                    timeout=10,
                )

                # rewind stream (good practice)
                image_file.stream.seek(0)

                if img_resp.status_code == 200:
                    image_url = img_resp.json().get("data", {}).get("image_url")
                else:
                    error = img_resp.json().get("message", "Image upload failed")
                    return render_template(
                        "admin_add_product.html",
                        categories=categories,
                        error=error,
                    )
            except Exception as e:
                return render_template(
                    "admin_add_product.html",
                    categories=categories,
                    error=str(e),
                )

        # Product payload
        data = {
            "name": name,
            "price": price,
            "stock": stock,
            "category_id": category_id,
            "description": description,
            "image_url": image_url,
        }

        # Create product
        try:
            resp = requests.post(
                f"{BACKEND_URL}/products/",
                headers=headers,
                json=data,
                timeout=10,
            )

            if resp.status_code == 200:
                return redirect(url_for("product.list_products"))
            else:
                error = resp.json().get("message", "Failed to add product")
                return render_template(
                    "admin_add_product.html",
                    categories=categories,
                    error=error,
                )
        except Exception as e:
            return render_template(
                "admin_add_product.html",
                categories=categories,
                error=str(e),
            )

    return render_template("admin_add_product.html", categories=categories)



@product_bp.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    headers = get_admin_headers()
    if not headers:
        return redirect(url_for("auth.login"))
    try:
        requests.delete(f"{BACKEND_URL}/products/{product_id}", headers=headers)
    except Exception:
        pass
    return redirect(url_for("product.list_products"))
