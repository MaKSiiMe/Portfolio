from flask import Blueprint, request, jsonify

from app.models.uno.deck import create_deck

from app.models.envs import UnoEnv

main = Blueprint('main', __name__)

@main.route('/api/create_deck', methods=['POST'])
def api_creat_deck():
    data = request.get_json() or {}
    seed = data.get('seed', None)

    deck = create_deck(seed)

    return jsonify({"deck": deck})

@main.route('/api/reshuffle", methods=['POST'])
def api_reshuffle():
    data = request.get_json()
    deck = data.get('deck', [])
    discard_pile = data.get('discard_pile', [])

    reshuffle_discard_pile(deck, discard_pile)

    return jsonify({"deck": deck, "discard_pile": discard_pile})
