from flask import Blueprint, jsonify, request
import uuid

from app.models.uno.game import Game
from app.models.uno.rules import is_playable

bp = Blueprint("api", __name__, url_prefix="/api")

games = {}

def api_response(success, data=None, error=None, code=200):
    if data is None:
        data = {}
    return jsonify({
        "success": success,
        "data": data,
        "error": error
    }), code

@bp.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json()
    num_players = data.get("num_players", 2)
    seed = data.get("seed")
    agent_type = data.get("agent_type", "rulesbased") # <--- Valeur par défaut

    if not isinstance(num_players, int) or num_players < 2 or num_players > 10:
        return api_response(False, error="num_players must be an integer between 2 and 10", code=400)

    if agent_type not in ["rulesbased", "random", "ppo"]:
        return api_response(False, error=f"Unknown agent_type: {agent_type}", code=400)

    game = Game(num_players=num_players, seed=seed, agent_type=agent_type)
    game.start()
    game_id = str(uuid.uuid4())
    games[game_id] = game

    return api_response(
        True,
        data={
            "game_id": game_id,
            "agent_type": agent_type,
            "message": f"Game started vs {agent_type} agent",
            "discard_pile": game.discard_pile[-1],
            "hands": [len(hand) for hand in game.hands],
            "state": game.get_state()
        }
    )

@bp.route("/game_state/<game_id>", methods=["GET"])
def game_state(game_id):
    game = games.get(game_id)
    if not game:
        return api_response(False, error="Invalid game_id", code=404)
    return api_response(True, data={"state": game.get_state()})

@bp.route("/play_turn", methods=["POST"])
def play_turn():
    data = request.get_json()
    game_id = data.get("game_id")
    human_input = data.get("human_input")

    game = games.get(game_id)
    if not game:
        return api_response(False, error="Invalid game_id", code=404)

    if human_input is not None:
        try:
            human_input = int(human_input)
        except Exception:
            return api_response(False, error="human_input must be an integer or null", code=400)

        hand = game.hands[game.current_player]
        if human_input < 0 or human_input >= len(hand):
            return api_response(False, error="human_input out of bounds", code=400)

    winner = game.play_turn(human_input=human_input)
    response = {
        "state": game.get_state(),
        "winner": winner,
        "scores": game.calculate_scores() if winner is not None else None
    }
    return api_response(True, data=response)


@bp.route("/is_playable", methods=["POST"])
def check_is_playable():
    data = request.get_json()
    card = data.get("card")
    top_card = data.get("top_card")
    current_color = data.get("current_color")

    if not card or not top_card or not current_color:
        return api_response(
            False, 
            error="Fields 'card', 'top_card' and 'current_color' are required", 
            code=400
        )

    playable = is_playable(card, top_card, current_color)
    return api_response(True, data={"playable": playable})

@bp.route("/delete_game/<game_id>", methods=["DELETE"])
def delete_game(game_id):
    if game_id in games:
        del games[game_id]
        return api_response(True, data={"message": f"Game {game_id} deleted."})
    else:
        return api_response(False, error="Invalid game_id", code=404)

@bp.route("/draw_cards", methods=["POST"])
def draw_cards():
    data = request.get_json()
    game_id = data.get("game_id")
    player_idx = data.get("player_idx")
    count = data.get("count", 1)

    game = games.get(game_id)
    if not game:
        return api_response(False, error="Invalid game_id", code=404)

    if not isinstance(player_idx, int) or player_idx < 0 or player_idx >= game.num_players:
        return api_response(False, error="Invalid player index", code=400)

    game.draw_cards(player_idx, count)
    return api_response(True, data={"state": game.get_state()})

@bp.route("/play_card", methods=["POST"])
def play_card():
    data = request.get_json()
    game_id = data.get("game_id")
    player_idx = data.get("player_idx")
    card = data.get("card")

    game = games.get(game_id)
    if not game:
        return api_response(False, error="Invalid game_id", code=404)

    if not isinstance(player_idx, int) or player_idx < 0 or player_idx >= game.num_players:
        return api_response(False, error="Invalid player index", code=400)

    hand = game.hands[player_idx]
    if card not in hand:
        return api_response(False, error="Card not in player hand", code=400)

    if not is_playable(card, game.discard_pile[-1]):
        return api_response(False, error="Card is not playable", code=400)

    hand.remove(card)
    game.discard_pile.append(card)
    # Effets spéciaux à externaliser dans Game si besoin

    return api_response(True, data={"state": game.get_state()})

@bp.route("/debug_agent/<game_id>", methods=["GET"])
def debug_agent(game_id):
    game = games.get(game_id)
    if not game:
        return api_response(False, error="Invalid game_id", code=404)
    agent_types = [type(a).__name__ if a is not None else "Human" for a in game.agents]
    return api_response(
        True,
        data={
            "agent_types": agent_types,
            "selected_agent_type": getattr(game, "agent_type", None)
        }
    )

@bp.route("/choose_color", methods=["POST"])
def choose_color():
    data = request.get_json()
    game_id = data.get("game_id")
    color = data.get("color")

    game = games.get(game_id)
    if not game:
        return api_response(False, error="Invalid game_id", code=404)

    if color not in ["Red", "Yellow", "Blue", "Green"]:
        return api_response(False, error="Invalid color", code=400)

    game.set_current_color(color)
    return api_response(True, data={"current_color": color})

@bp.route("/get_scores/<game_id>", methods=["GET"])
def get_scores(game_id):
    game = games.get(game_id)
    if not game:
        return api_response(False, error="Invalid game_id", code=404)
    scores = game.calculate_scores()
    return api_response(True, data={"scores": scores})
