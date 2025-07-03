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


@bp.route("/draw_cards", methods=["POST"])
def draw_cards():
    data = request.get_json()
    game_id = data.get("game_id")
    player_idx = data.get("player_idx")
    count = data.get("count", 1)

    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Invalid game_id"}), 404

    if not isinstance(player_idx, int) or player_idx < 0 or player_idx >= game.num_players:
        return jsonify({"error": "Invalid player index"}), 400

    game.draw_cards(player_idx, count)

    # ✅ Après que le joueur pioche, faire avancer le tour et jouer le bot
    game.advance_turn()
    game.play_bot_turn()

    return jsonify({"state": game.get_state()})


@bp.route("/play_card", methods=["POST"])
def play_card():
    data = request.get_json()
    game_id = data.get("game_id")
    player_idx = data.get("player_idx")
    card = data.get("card")
    chosen_color = data.get("chosen_color")  # <-- On récupère la couleur choisie

    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Invalid game_id"}), 404

    if not isinstance(player_idx, int) or player_idx < 0 or player_idx >= game.num_players:
        return jsonify({"error": "Invalid player index"}), 400

    # Cherche et joue la carte
    hand = game.hands[player_idx]
    if card not in hand:
        return jsonify({"error": "Card not in player hand"}), 400

    if not is_playable(card, game.discard_pile[-1]):
        return jsonify({"error": "Card is not playable"}), 400

    hand.remove(card)

    # Si c’est une carte Wild ou Wild +4, appliquer la couleur choisie
    if "Wild" in card:
        if not chosen_color:
            return jsonify({"error": "Missing chosen_color for Wild card"}), 400
        card = f"{chosen_color} {card.split(' ', 1)[1]}"  # Exemple : "black Wild +4" -> "blue Wild +4"

        # Gérer les effets spéciaux ici
        if "+4" in card:
            game.draw_four_next += 1

    game.discard_pile.append(card)

    # Effets supplémentaires
    if "+2" in card:
        game.draw_two_next += 1
    elif "Skip" in card:
        game.skip_next = True
    elif "Reverse" in card:
        if game.num_players == 2:
            game.skip_next = True
        else:
            game.direction *= -1
    # Avance le tour et joue le bot
    game.advance_turn()
    game.play_bot_turn()

    return jsonify({"state": game.get_state()})

@bp.route("/bot_play", methods=["POST"])
def bot_play():
    game_id = request.args.get("game_id")
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Invalid game_id"}), 404

    game.play_bot_turn()
    return jsonify(game.get_state())