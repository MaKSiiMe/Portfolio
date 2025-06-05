"""
UNO Game Module

This module implements a simple UNO game simulation. It includes the creation of the deck,
game logic, and basic user interactions for a single human player against AI players.
"""

import random
import time
import sys
from typing import List, Optional

COLORS = ['Red', 'Green', 'Blue', 'Yellow']
VALUES = list(range(1, 10))
SPECIAL_CARDS = ['+2', 'Reverse', 'Skip']
CARDS_PER_PLAYER = 7
NUM_PLAYERS = 3

if NUM_PLAYERS > 10:
    print("Le nombre maximum de joueurs autorisé est 10.")
    sys.exit(1)

PLAYER_NAMES = [f"Joueur {i}" for i in range(NUM_PLAYERS)]
HUMAN_PLAYER_IDX = 0

def create_deck(seed: Optional[int] = None) -> List[str]:
    """
    Create and shuffle the UNO deck.

    Args:
        seed (Optional[int]): Seed for random shuffling.

    Returns:
        List[str]: Shuffled deck of UNO cards.
    """
    deck = []
    for color in COLORS:
        deck.append(f"{color} 0")
    for color in COLORS:
        for value in VALUES:
            deck.extend([f"{color} {value}"] * 2)
    for color in COLORS:
        for special in SPECIAL_CARDS:
            deck.extend([f"{color} {special}"] * 2)
    deck.extend(['Wild'] * 4)
    deck.extend(['Wild +4'] * 4)
    random.seed(seed if seed is not None else time.time())
    random.shuffle(deck)
    return deck

def is_playable(card: str, top_card: str) -> bool:
    """
    Check if a card is playable on the current top card.

    Args:
        card (str): The card to check.
        top_card (str): The current top card on the discard pile.

    Returns:
        bool: True if the card is playable, False otherwise.
    """
    card_parts = card.split()
    top_parts = top_card.split()
    if card_parts[0] == 'Wild':
        return True
    return card_parts[0] == top_parts[0] or card_parts[1] == top_parts[1]

def print_hand(player_idx: int, hand: List[str]) -> None:
    """
    Print the hand of a player.

    Args:
        player_idx (int): The index of the player.
        hand (List[str]): The hand of the player.
    """
    print(f"{PLAYER_NAMES[player_idx]}: {hand}")

def print_board(turn: int, current_player: int, top_card: str) -> None:
    """
    Print the current state of the game board.

    Args:
        turn (int): The current turn number.
        current_player (int): The index of the current player.
        top_card (str): The current top card on the discard pile.
    """
    print(f"\nTour {turn} - Tour de {PLAYER_NAMES[current_player]}")
    print(f"Carte du dessus: {top_card}")

def main(seed: Optional[int] = None) -> None:
    """
    Main function to run the UNO game.

    Args:
        seed (Optional[int]): Seed for random shuffling.
    """
    if seed is None and len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            print("Usage : python main.py [seed]")
            sys.exit(1)

    deck = create_deck(seed)
    hands = [deck[i * CARDS_PER_PLAYER:(i + 1) * CARDS_PER_PLAYER] for i in range(NUM_PLAYERS)]
    deck = deck[CARDS_PER_PLAYER * NUM_PLAYERS:]
    discard_pile = [deck.pop()]

    if discard_pile[-1].startswith("Wild"):
        new_color = random.choice(COLORS)
        if "+4" in discard_pile[-1]:
            discard_pile[-1] = f"{new_color} Wild +4"
            draw_four_next = 1
            print(f"Première carte: Wild +4 -> la couleur devient {new_color}, le premier joueur devra piocher 4 cartes")
        else:
            discard_pile[-1] = f"{new_color} Wild"
            print(f"Première carte: Wild -> la couleur devient {new_color}")

    turn = 0
    current_player = 0
    consecutive_passes = 0
    draw_two_next = 0
    draw_four_next = 0
    skip_next = False
    direction = 1
    skip_current_player = False

    while all(len(hand) > 0 for hand in hands):
        print_board(turn, current_player, discard_pile[-1])
        print_hand(current_player, hands[current_player])

        if draw_four_next:
            for _ in range(4):
                if deck:
                    hands[current_player].append(deck.pop())
            print(f"{PLAYER_NAMES[current_player]} pioche 4 cartes (effet +4)")
            draw_four_next = 0
            skip_current_player = True

        elif draw_two_next > 0:
            cards_to_draw = 2 * draw_two_next
            for _ in range(cards_to_draw):
                if deck:
                    hands[current_player].append(deck.pop())
                else:
                    print(f"{PLAYER_NAMES[current_player]} aurait dû piocher {cards_to_draw} cartes mais la pioche est vide")
                    break
            print(f"{PLAYER_NAMES[current_player]} pioche {cards_to_draw} cartes (effet +2)")
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

        playable_cards = [card for card in hands[current_player] if is_playable(card, discard_pile[-1])]

        if current_player == HUMAN_PLAYER_IDX:
            print("Vos cartes :", hands[current_player])
            print("Carte sur le dessus :", discard_pile[-1])
            if not playable_cards:
                input("Vous ne pouvez pas jouer, appuyez sur Entrée pour piocher une carte...")
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
                    choice = input(f"Quelle carte voulez-vous jouer ? (0-{len(playable_cards)-1}): ")
                    if choice.isdigit() and 0 <= int(choice) < len(playable_cards):
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
                        elif card_to_play.startswith("Wild") and "+4" not in card_to_play:
                            new_color = random.choice(COLORS)
                            discard_pile[-1] = f"{new_color} Wild"
                            print(f"Vous changez la couleur en {new_color}")
                        elif "Wild +4" in card_to_play:
                            new_color = random.choice(COLORS)
                            discard_pile[-1] = f"{new_color} Wild +4"
                            draw_four_next += 1
                            print(f"Vous changez la couleur en {new_color} et infligez +4")
                        break
                    else:
                        print("Choix invalide.")
        else:
            if playable_cards:
                card_to_play = playable_cards[0]
                hands[current_player].remove(card_to_play)
                discard_pile.append(card_to_play)
                print(f"{PLAYER_NAMES[current_player]} joue {card_to_play}")
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
                elif card_to_play.startswith("Wild") and "+4" not in card_to_play:
                    new_color = random.choice(COLORS)
                    discard_pile[-1] = f"{new_color} Wild"
                    print(f"{PLAYER_NAMES[current_player]} change la couleur en {new_color}")
                elif "Wild +4" in card_to_play:
                    new_color = random.choice(COLORS)
                    discard_pile[-1] = f"{new_color} Wild +4"
                    draw_four_next += 1
                    print(f"{PLAYER_NAMES[current_player]} change la couleur en {new_color} et inflige +4")
            else:
                if deck:
                    drawn_card = deck.pop()
                    hands[current_player].append(drawn_card)
                    print(f"{PLAYER_NAMES[current_player]} pioche une carte")
                    consecutive_passes = 0
                else:
                    print(f"{PLAYER_NAMES[current_player]} ne peut pas piocher, le paquet est vide")
                    consecutive_passes += 1

        if consecutive_passes >= NUM_PLAYERS:
            print("\nAucun joueur ne peut jouer, le paquet est vide. Match nul.")
            return

        current_player = (current_player + direction) % NUM_PLAYERS
        turn += 1

    winner = next(i for i, hand in enumerate(hands) if len(hand) == 0)
    print(f"\n{PLAYER_NAMES[winner]} a gagné !")

if __name__ == "__main__":
    main()
