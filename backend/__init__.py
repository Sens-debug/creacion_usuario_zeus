from flask import Flask
from backend.Routes.form_routes import user_bp

def crear_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    return app