"""
main.py

UNO Card Game

This module implements a simple UNO card game with multiple players.
"""

import sys
import random
from typing import Optional

from uno.constants import (
    COLORS, VALUES, SPECIAL_CARDS, WILD_CARDS, CARDS_PER_PLAYER, MAX_PLAYERS
)
from uno.deck import create_deck, reshuffle_discard_pile
from uno.rules import is_playable, calculate_score
from uno.display import print_board, print_hand


NUM_PLAYERS = 2  # Configurable
HUMAN_PLAYER_IDX = -1  # Par défaut aucun joueur humain

if NUM_PLAYERS > 10:
    print("Le nombre maximum de joueurs autorisé est 10.")
    sys.exit(1)

PLAYER_NAMES = [f"Joueur {i}" for i in range(NUM_PLAYERS)]


def main(seed: Optional[int] = None) -> None:
    """
    Main function to run the UNO game.

    Args:
        seed (Optional[int]): Seed for random number generation.
    """
    if seed is None and len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            print("Usage : python main.py [seed]")
            sys.exit(1)

    scores = [0] * NUM_PLAYERS
    game_number = 1

    while max(scores) < 500:
        print(f"\n=== Manche {game_number} ===")
        deck = create_deck(seed)
        hands = [
            deck[i * CARDS_PER_PLAYER:(i + 1) * CARDS_PER_PLAYER]
            for i in range(NUM_PLAYERS)
        ]
        deck = deck[CARDS_PER_PLAYER * NUM_PLAYERS:]
        discard_pile = [deck.pop()]

        if discard_pile[-1].startswith("Wild"):
            new_color = random.choice(COLORS)
            if "+4" in discard_pile[-1]:
                discard_pile[-1] = f"{new_color} Wild +4"
                draw_four_next = 1
                print(
                    f"Première carte: Wild +4 -> la couleur devient "
                    f"{new_color}, le premier joueur devra piocher 4 cartes"
                )
            else:
                discard_pile[-1] = f"{new_color} Wild"
                print(
                    f"Première carte: Wild -> la couleur devient {new_color}"
                )

        turn = 0
        current_player = 0
        consecutive_passes = 0
        draw_two_next = 0
        draw_four_next = 0
        skip_next = False
        direction = 1
        skip_current_player = False

        while True:
            if any(len(hand) == 0 for hand in hands):
                break

            print_board(turn, current_player, discard_pile[-1])
            print_hand(current_player, hands[current_player])

            if draw_four_next:
                for _ in range(4):
                    if not deck:
                        reshuffle_discard_pile(deck, discard_pile)
                    if deck:
                        hands[current_player].append(deck.pop())
                print(
                    f"{PLAYER_NAMES[current_player]} "
                    f"pioche 4 cartes (effet +4)"
                )
                draw_four_next = 0
                skip_current_player = True

            elif draw_two_next > 0:
                cards_to_draw = 2 * draw_two_next
                for _ in range(cards_to_draw):
                    if not deck:
                        reshuffle_discard_pile(deck, discard_pile)
                    if deck:
                        hands[current_player].append(deck.pop())
                print(
                    f"{PLAYER_NAMES[current_player]} pioche {cards_to_draw} "
                    "(effet +2)"
                )
                draw_two_next = 0
                skip_current_player = True

            elif skip_next:
                print(f"{PLAYER_NAMES[current_player]} est passé (Skip)")
                skip_next = False
                skip_current_player = True

            if skip_current_player:
                skip_current_player = False
                consecutive_passes = 0
                current_player = (current_player + direction) % NUM_PLAYERS
                turn += 1
                continue

            playable_cards = [
                card for card in hands[current_player]
                if is_playable(card, discard_pile[-1])
            ]

            if current_player == HUMAN_PLAYER_IDX:
                print("Vos cartes :", hands[current_player])
                print("Carte sur le dessus :", discard_pile[-1])
                if not playable_cards:
                    input(
                        "Vous ne pouvez pas jouer, appuyez sur Entrée pour "
                        "piocher une carte..."
                    )
                    if not deck:
                        reshuffle_discard_pile(deck, discard_pile)
                    if deck:
                        drawn = deck.pop()
                        print("Vous avez pioché :", drawn)
                        hands[current_player].append(drawn)
                    else:
                        print("La pioche est vide.")
                        consecutive_passes += 1
                else:
                    print("Cartes jouables :", playable_cards)
                    while True:
                        choice = input(
                            f"Quelle carte voulez-vous jouer ? "
                            f"(0-{len(playable_cards)-1}): "
                        )
                        if (
                            choice.isdigit() and
                            0 <= int(choice) < len(playable_cards)
                        ):
                            card_to_play = playable_cards[int(choice)]
                            hands[current_player].remove(card_to_play)
                            discard_pile.append(card_to_play)
                            print(f"Vous jouez {card_to_play}")
                            if "+2" in card_to_play:
                                draw_two_next += 1
                            elif "Skip" in card_to_play:
                                skip_next = True
                            elif "Reverse" in card_to_play:
                                if NUM_PLAYERS == 2:
                                    skip_next = True
                                else:
                                    direction *= -1
                                    print("Sens de jeu inversé !")
                            elif (
                                card_to_play.startswith("Wild") and
                                "+4" not in card_to_play
                            ):
                                new_color = random.choice(COLORS)
                                discard_pile[-1] = f"{new_color} Wild"
                                print(
                                    f"Vous changez la couleur en {new_color}"
                                )
                            elif "Wild +4" in card_to_play:
                                new_color = random.choice(COLORS)
                                discard_pile[-1] = f"{new_color} Wild +4"
                                draw_four_next += 1
                                print(
                                    f"Vous changez la couleur en {new_color} "
                                    "et infligez +4"
                                )
                            break
                        else:
                            print("Choix invalide.")
            else:
                if playable_cards:
                    card_to_play = playable_cards[0]
                    hands[current_player].remove(card_to_play)
                    discard_pile.append(card_to_play)
                    print(
                        f"{PLAYER_NAMES[current_player]} joue {card_to_play}"
                    )
                    consecutive_passes = 0
                    if "+2" in card_to_play:
                        draw_two_next += 1
                    elif "Skip" in card_to_play:
                        skip_next = True
                    elif "Reverse" in card_to_play:
                        if NUM_PLAYERS == 2:
                            skip_next = True
                        else:
                            direction *= -1
                            print("Sens de jeu inversé !")
                    elif (
                        card_to_play.startswith("Wild") and
                        "+4" not in card_to_play
                    ):
                        new_color = random.choice(COLORS)
                        discard_pile[-1] = f"{new_color} Wild"
                        print(
                            f"{PLAYER_NAMES[current_player]} change la "
                            f"couleur en {new_color}"
                        )
                    elif "Wild +4" in card_to_play:
                        new_color = random.choice(COLORS)
                        discard_pile[-1] = f"{new_color} Wild +4"
                        draw_four_next += 1
                        print(
                            f"{PLAYER_NAMES[current_player]} change la "
                            f"couleur en {new_color} et inflige +4"
                        )
                else:
                    if not deck:
                        reshuffle_discard_pile(deck, discard_pile)
                    if deck:
                        drawn_card = deck.pop()
                        hands[current_player].append(drawn_card)
                        print(
                            f"{PLAYER_NAMES[current_player]} pioche une carte"
                        )
                        consecutive_passes = 0
                    else:
                        print(
                            f"{PLAYER_NAMES[current_player]} ne peut pas "
                            "piocher, le paquet est vide"
                        )
                        consecutive_passes += 1

            if consecutive_passes >= NUM_PLAYERS:
                print(
                    "\nAucun joueur ne peut jouer, le paquet est vide. "
                    "Match nul."
                )
                return

            current_player = (current_player + direction) % NUM_PLAYERS
            turn += 1

        winner = next(i for i, hand in enumerate(hands) if len(hand) == 0)
        points = calculate_score(hands, winner)
        scores[winner] += points

        print(
            f"\n{PLAYER_NAMES[winner]} remporte la manche et gagne "
            f"{points} points."
        )
        print("Scores actuels :")
        for i, score in enumerate(scores):
            print(f"  {PLAYER_NAMES[i]} : {score} points")

        game_number += 1

    final_winner = scores.index(max(scores))
    print(
        f"\n🎉 {PLAYER_NAMES[final_winner]} remporte la partie avec "
        f"{scores[final_winner]} points en {game_number} manches !"
    )


if __name__ == "__main__":
    main()
