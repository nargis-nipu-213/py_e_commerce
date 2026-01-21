from flask import Flask, session, redirect, url_for, render_template
from modules.auth_module import auth_bp
from modules.product_module import product_bp
from modules.cart_module import cart_bp
from modules.order_module import order_bp
import requests

app = Flask(__name__)
app.secret_key = "college_project_secret"

BACKEND_URL = "http://127.0.0.1:5000"

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(cart_bp, url_prefix="/cart")
app.register_blueprint(order_bp, url_prefix="/orders")

# ---------------------------
# Dashboard Route (User-Facing)
# ---------------------------
@app.route("/")
def dashboard():
    user = session.get("user")
    if not user:
        return redirect(url_for("auth.login"))

    BASE_URL = "http://127.0.0.1:5000"  # backend base URL

    try:
        # Fetch categories
        resp_cat = requests.get(f"{BASE_URL}/categories/")
        categories = resp_cat.json().get("data", [])

        # Fetch products
        resp_prod = requests.get(f"{BASE_URL}/products/")
        products = resp_prod.json().get("data", [])

        # Prepend base URL to image_url if exists
        for p in products:
            if p.get("image_url"):
                if not p["image_url"].startswith("http"):
                    p["image_url"] = BASE_URL + p["image_url"]

    except Exception as e:
        print("Error fetching dashboard data:", e)
        categories = []
        products = []

    return render_template("dashboard.html", user=user, categories=categories, products=products)



# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(port=5001, debug=True, use_reloader=False)
