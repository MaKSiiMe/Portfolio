from flask import Blueprint, jsonify, request
import uuid

from app.models.uno.game import Game
from app.models.uno.rules import is_playable

bp = Blueprint("api", __name__, url_prefix="/api")

# Stocke les parties en cours avec leurs game_id
games = {}


@bp.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json()
    num_players = data.get("num_players", 2)
    seed = data.get("seed")

    game = Game(num_players=num_players, seed=seed)
    game.start()

    game_id = str(uuid.uuid4())
    games[game_id] = game

    return jsonify({
        "game_id": game_id,
        "message": "Game started",
        "discard_pile": game.discard_pile[-1],
        "hands": [len(hand) for hand in game.hands]
    })


@bp.route("/game_state/<game_id>", methods=["GET"])
def game_state(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Invalid game_id"}), 404

    return jsonify(game.get_state())


@bp.route("/play_turn", methods=["POST"])
def play_turn():
    data = request.get_json()
    game_id = data.get("game_id")
    human_input = data.get("human_input")

    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Invalid game_id"}), 404

    winner = game.play_turn(human_input=human_input)

    response = {
        "state": game.get_state(),
        "winner": winner,
        "scores": game.calculate_scores() if winner is not None else None
    }
    return jsonify(response)


@bp.route("/is_playable", methods=["POST"])
def check_is_playable():
    data = request.get_json()
    card = data.get("card")
    top_card = data.get("top_card")

    if not card or not top_card:
        return jsonify({"error": "Both 'card' and 'top_card' are required"}), 400

    return jsonify({"playable": is_playable(card, top_card)})


@bp.route("/delete_game/<game_id>", methods=["DELETE"])
def delete_game(game_id):
    if game_id in games:
        del games[game_id]
        return jsonify({"message": f"Game {game_id} deleted."})
    else:
        return jsonify({"error": "Invalid game_id"}), 404
