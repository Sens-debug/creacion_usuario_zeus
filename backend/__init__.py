from flask import Flask
from backend.Routes.form_routes import form_bp

def crear_app():
    app = Flask(__name__)
    app.register_blueprint(form_bp)


    return app