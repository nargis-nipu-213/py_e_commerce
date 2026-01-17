from flask import Blueprint, render_template, session, redirect, url_for
import requests

cart_bp = Blueprint("cart", __name__, template_folder="../templates")
BACKEND_URL = "http://127.0.0.1:5000"

def get_user_id():
    user = session.get("user")
    return user["id"] if user else None

def fetch_product_details(product_id):
    """Fetch product info from backend"""
    try:
        resp = requests.get(f"{BACKEND_URL}/products/{product_id}", timeout=5)
        data = resp.json().get("data")
        if data:
            # Prepend base URL to image
            if data.get("image_url") and not data["image_url"].startswith("http"):
                data["image_url"] = BACKEND_URL + data["image_url"]
            return data
    except:
        pass
    return {"name": "Unknown", "price": 0, "image_url": None}

# -------------------------------
# View cart page
# -------------------------------
@cart_bp.route("/", methods=["GET"])
def view_cart():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))

    error = None
    message = None
    cart_items = []
    total_price = 0.0

    try:
        # Get cart items
        resp = requests.get(f"{BACKEND_URL}/cart/{user_id}", timeout=5)
        cart = resp.json().get("data", [])

        for item in cart:
            product_id = item.get("product_id") or item.get("id")
            quantity = int(item.get("quantity") or item.get("qty") or 0)

            # Fetch product info
            try:
                prod_resp = requests.get(f"{BACKEND_URL}/products/{product_id}", timeout=5)
                prod_data = prod_resp.json().get("data", {})
            except:
                prod_data = {}

            price = float(prod_data.get("price") or 0)
            name = prod_data.get("name") or "Unknown"
            image_url = prod_data.get("image_url")
            if image_url and not image_url.startswith("http"):
                image_url = BACKEND_URL + image_url

            # Append normalized item
            cart_items.append({
                "product_id": product_id,
                "product_name": name,
                "price": price,
                "quantity": quantity,
                "image_url": image_url
            })

            # Update total
            total_price += price * quantity

    except Exception as e:
        cart_items = []
        error = str(e)

    # Pass total_price to template
    return render_template("cart.html", cart=cart_items, error=error, message=message, total_price=round(total_price, 2))


# -------------------------------
# Add item to cart
# -------------------------------
@cart_bp.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))

    try:
        requests.post(
            f"{BACKEND_URL}/cart/{user_id}",
            json={"product_id": product_id, "quantity": 1},
            timeout=5
        )
    except Exception as e:
        print("Error adding to cart:", e)

    return redirect(url_for("cart.view_cart"))

# -------------------------------
# Remove item from cart
# -------------------------------
@cart_bp.route("/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))

    try:
        requests.delete(f"{BACKEND_URL}/cart/{user_id}/{product_id}", timeout=5)
    except Exception as e:
        print("Error removing from cart:", e)

    return redirect(url_for("cart.view_cart"))
