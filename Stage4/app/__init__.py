from flask import Flask
from flask_cors import CORS  # pour corriger le CORS
from app.v1.routes import bp  # importe ton Blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)  # autorise toutes les origines (simple pour développement)

    app.register_blueprint(bp)  # enregistre les routes

    return app

