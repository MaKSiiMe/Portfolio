from flask import Blueprint, request, jsonify
from app.models.uno import deck, rules
from app.models.envs import UnoEnv

main = Blueprint('main', __name__)

uno = UnoEnv()

@main.route('/api/play', methods=['POST'])
def play():
    data = request.get_json()
    move = data.get('move')

    result = {"message": f"Received move: {move}"}

    return jsonify(response)

@main.route('/api/index', methods=['POST'])
def index():
    return "UNO API is running!"
