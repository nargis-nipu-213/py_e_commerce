from flask import Flask, send_from_directory
from flask_cors import CORS
from routes import register_routes
import os

app = Flask(__name__)
CORS(app)

# Serve uploaded images
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads", "images")

@app.route("/uploads/images/<filename>")
def uploaded_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Register all blueprints/routes
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
