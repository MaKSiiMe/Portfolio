"""
display.py

This module provides functions to print the current state of the game,
including player hands and the board state.
"""

from typing import List


def print_board(turn: int, current_player: int, top_card: str, deck_size: int = None) -> None:
    """
    Print the current state of the board.

    Args:
        turn (int): The current turn number.
        current_player (int): The index of the current player.
        top_card (str): The top card on the discard pile.
        deck_size (int, optional): The size of the deck. Defaults to None.
    """
    print(f"\nTurn {turn} - Player {current_player}'s turn")
    print(f"Top card: {top_card}")
    if deck_size is not None:
        print(f"Deck size: {deck_size}")

def print_hand(player_idx, hand):
    """
    Print the hand of a player (for human interaction).

    Args:
        player_idx (int): The index of the player.
        hand (List[str]): The cards in the player's hand.
    """
    print(f"Player {player_idx}: {', '.join(hand)}")
