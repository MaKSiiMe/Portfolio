"""
display.py

This module provides functions to print the current state of the game,
including player hands and the board state.
"""

from typing import List
from .constants import PLAYER_NAMES


def print_hand(player_idx: int, hand: List[str]) -> None:
    """
    Print the hand of a player.

    Args:
        player_idx (int): The index of the player.
        hand (List[str]): The list of cards in the player's hand.
    """
    print(f"{PLAYER_NAMES[player_idx]}: {', '.join(hand)}")


def print_board(turn: int, current_player: int, top_card: str) -> None:
    """
    Print the current state of the board.

    Args:
        turn (int): The current turn number.
        current_player (int): The index of the current player.
        top_card (str): The top card on the discard pile.
    """
    print(f"\nTour {turn} - Tour de {PLAYER_NAMES[current_player]}")
    print(f"Carte du dessus: {top_card}")
