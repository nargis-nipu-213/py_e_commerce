from flask import Flask, session, redirect, url_for, render_template
from modules.auth_module import auth_bp
from modules.product_module import product_bp
from modules.category_module import category_bp
from modules.order_module import order_bp

app = Flask(__name__)
app.secret_key = "secret_key"

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(category_bp, url_prefix="/categories")
app.register_blueprint(order_bp, url_prefix="/orders")

@app.route("/")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("auth.login"))
    return render_template("admin_dashboard.html", admin=session["admin"])

if __name__ == "__main__":
    app.run(port=5002, debug=True, use_reloader=False)
