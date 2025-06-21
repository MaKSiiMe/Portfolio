from flask import Blueprint, request, jsonify

from app.models.uno.game import Game

from app.models.uno.deck import create_deck
from app.models.uno.deck import reshuffle_discard_pile

from app.models.envs.uno_env import UnoEnv

main = Blueprint('main', __name__)
game = Game(num_players=2)


@main.route("/", methods=["GET"])
def index():
    return "API UNO OK"

@main.route('/api/new_game', methods=['POST'])
def new_game():
    global game
    game = Game(num_players=2)
    game.start()
    return jsonify({"message": "New game started", "state": game.get_state()})

@main.route('/api/game_state', methods=['GET'])
def game_state():
        return jsonify(game.get_state())


@main.route('/api/create_deck', methods=['POST'])
def api_creat_deck():
    data = request.get_json() or {}
    seed = data.get('seed', None)

    deck = create_deck(seed)

    return jsonify({"deck": deck})

@main.route('/api/reshuffle', methods=['POST'])
def api_reshuffle():
    data = request.get_json()
    deck = data.get('deck', [])
    discard_pile = data.get('discard_pile', [])

    reshuffle_discard_pile(deck, discard_pile)

    return jsonify({"deck": deck, "discard_pile": discard_pile})
