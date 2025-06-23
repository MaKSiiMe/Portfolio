import requests
import time

BASE_URL = "http://127.0.0.1:5000/api"

def start_game(num_players=2, seed=None):
    payload = {"num_players": num_players}
    if seed is not None:
        payload["seed"] = seed
    response = requests.post(f"{BASE_URL}/start_game", json=payload)
    return response.json()

def get_game_state(game_id):
    response = requests.get(f"{BASE_URL}/game_state/{game_id}")
    return response.json()

def play_turn(game_id):
    payload = {"game_id": game_id}
    response = requests.post(f"{BASE_URL}/play_turn", json=payload)
    return response.json()

def print_hand_summary(hands):
    for idx, hand in enumerate(hands):
        print(f"  Joueur {idx} [{len(hand)} cartes] : {', '.join(hand)}")

if __name__ == "__main__":
    # Lancement de la partie
    num_players = 2
    seed = 42  # Optionnel pour reproductibilité
    game = start_game(num_players=num_players, seed=seed)
    game_id = game["game_id"]
    print(f"Nouvelle partie UNO lancée avec ID: {game_id}\n")

    # Boucle jusqu'à la fin de la partie
    while True:
        result = play_turn(game_id)
        state = result["state"]
        print(f"Tour {state['turn']} - Joueur courant : {state['current_player']}")
        print(f"Carte sur le dessus : {state['discard_pile'][-1]}")
        print(f"Nombre de cartes restantes dans le deck : {state['deck_size']}")
        print("Mains actuelles des joueurs :")
        print_hand_summary(state["hands"])
        print("-" * 80)

        if result.get("winner") is not None:
            print("🏆 Partie terminée 🏆")
            print(f"Gagnant : Joueur {result['winner']}")
            print(f"Scores : {result['scores']}")
            break

        time.sleep(0.2)
