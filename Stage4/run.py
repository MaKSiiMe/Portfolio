"""
run.py

UNO Command-Line Game using the Game class.
"""

import sys
from typing import Optional

from app.models.uno.game import Game
from app.models.uno.display import print_board, print_hand


NUM_PLAYERS = 3  # Configurable
HUMAN_PLAYER_IDX = -1  # Indice du joueur humain


def main(seed: Optional[int] = None):
    if seed is None and len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            print("Usage : python run.py [seed]")
            sys.exit(1)

    game = Game(num_players=NUM_PLAYERS, seed=seed)
    game.start()

    print(f"\n=== Début de la partie UNO ===\n")
    print(f"Première carte : {game.discard_pile[-1]}")

    while True:
        print_board(game.turn, game.current_player, game.discard_pile[-1])
        print_hand(game.current_player, game.hands[game.current_player])

        if game.current_player == HUMAN_PLAYER_IDX:
            playable = [
                card for card in game.hands[game.current_player]
                if game.discard_pile and
                   (card.split()[0] == game.discard_pile[-1].split()[0] or
                    card.split()[1] == game.discard_pile[-1].split()[1] or
                    card.startswith("Wild"))
            ]
            if playable:
                print("Cartes jouables :", playable)
                while True:
                    choice = input(f"Quelle carte voulez-vous jouer ? (0-{len(playable)-1} ou 'p' pour piocher) : ")
                    if choice == 'p':
                        winner = game.play_turn(human_input=None)
                        break
                    elif choice.isdigit() and 0 <= int(choice) < len(playable):
                        winner = game.play_turn(human_input=int(choice))
                        break
                    else:
                        print("Choix invalide.")
            else:
                input("Aucune carte jouable. Appuyez sur Entrée pour piocher...")
                winner = game.play_turn(human_input=None)
        else:
            winner = game.play_turn()

        if winner == -1:
            print("\nMatch nul ! Plus de cartes jouables.")
            break
        elif winner is not None:
            print(f"\n🎉 Joueur {winner} a gagné ! 🎉")
            break

    print("\nPartie terminée.")


if __name__ == "__main__":
    main()
