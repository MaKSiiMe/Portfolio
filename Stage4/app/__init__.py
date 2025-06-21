from flask import Flask
from flask_cors import CORS
from .v1.routes import bp as api_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api_bp)
    return app
