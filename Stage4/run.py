"""
UNO Game Script

This script implements a game of UNO for a specified number of players. It allows
for both human and AI players to participate, with a target score to determine the
winner across multiple rounds.
"""

import sys
from typing import List, Optional

from app.models.uno.game import Game
from app.models.uno.display import print_board, print_hand  # <-- ici
from app.models.agents.human_agent import ask_playable_choice, ask_draw

NUM_PLAYERS = 3
HUMAN_PLAYER_IDX = -1  # Index du joueur humain (0 pour le premier joueur)
TARGET_SCORE = 500

def main(seed: Optional[int] = None) -> None:
    """
    Main function to run the UNO game.

    Args:
        seed (Optional[int]): Seed for random number generation to ensure reproducibility.
    """
    if seed is None and len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            print("Usage: python run.py [seed]")
            sys.exit(1)

    scores: List[int] = [0] * NUM_PLAYERS
    game_number: int = 1

    while max(scores) < TARGET_SCORE:
        print(f"\n=== Round {game_number} ===")
        game = Game(num_players=NUM_PLAYERS, seed=seed)
        game.start()
        print(f"First card: {game.discard_pile[-1]}")

        while True:
            print_board(game.turn, game.current_player, game.discard_pile[-1], len(game.deck))
            print_hand(game.current_player, game.hands[game.current_player])

            card_played = None
            player_playing = game.current_player

            if game.current_player == HUMAN_PLAYER_IDX:
                playable = [
                    card for card in game.hands[game.current_player]
                    if game.discard_pile and
                       (
                           card.split()[0] == game.discard_pile[-1].split()[0] or
                           (len(card.split()) > 1 and len(game.discard_pile[-1].split()) > 1 and card.split()[1] == game.discard_pile[-1].split()[1]) or
                           card.startswith("Wild")
                       )
                ]
                if playable:
                    print("Playable cards:", playable)
                    while True:
                        choice = ask_playable_choice(playable)
                        if choice is None:
                            winner = game.play_turn(human_input=None)
                            card_played = None
                            break
                        else:
                            card_played = playable[choice]
                            winner = game.play_turn(human_input=choice)
                            break
                else:
                    ask_draw()
                    winner = game.play_turn(human_input=None)
                    card_played = None
            else:
                winner = game.play_turn()

            if card_played is not None:
                print(f"Player {player_playing} plays: {card_played}")

            if winner is not None:
                print(f"\n🎉 Player {winner} wins the round! 🎉")
                break

        round_scores = game.calculate_scores()
        if winner != -1:
            scores[winner] += round_scores[winner]

        print("\nRemaining cards for other players:")
        for i in range(NUM_PLAYERS):
            if i != winner:
                print(f"Player {i}: {game.hands[i]}")

        if winner != -1:
            print(f"\nPlayer {winner} earns {round_scores[winner]} points.")
        else:
            print("\nNo points awarded. The round ended in a draw.")

        print("\nCurrent scores:")
        for i, s in enumerate(scores):
            print(f"Player {i}: {s} points")

        game_number += 1

    winner = scores.index(max(scores))
    print(f"\n🏆 Player {winner} wins the game with {scores[winner]} points in {game_number - 1} rounds!")

if __name__ == "__main__":
    main()
    main()
