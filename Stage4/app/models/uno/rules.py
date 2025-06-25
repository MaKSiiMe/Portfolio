"""
rules.py

This module contains functions to determine the playability of cards and
calculate scores in a UNO game.
"""

from typing import List


def is_playable(card: str, top_card: str) -> bool:
    """
    Determine if a card is playable on the top card.

    Args:
        card (str): The card to check.
        top_card (str): The top card of the discard pile.

    Returns:
        bool: True if the card is playable, False otherwise.
    """
    card_parts = card.split()
    top_parts = top_card.split()

    if card_parts[0] == 'Wild':
        return True
    if len(card_parts) < 2 or len(top_parts) < 2:
        return False
    return card_parts[0] == top_parts[0] or card_parts[1] == top_parts[1]


def calculate_card_points(card: str) -> int:
    """
    Calculate the points of a given card.

    Args:
        card (str): The card to calculate points for.

    Returns:
        int: The points of the card.
    """
    if card.startswith("Wild"):
        return 50
    elif "+2" in card or "Skip" in card or "Reverse" in card:
        return 20
    else:
        try:
            return int(card.split()[1])
        except (IndexError, ValueError):
            return 0


def calculate_score(hands: List[List[str]], winner_idx: int) -> int:
    """
    Calculate the total score of the game by summing the points of the
    remaining cards in all hands except the winner's.

    Args:
        hands (List[List[str]]): A list of hands, where each hand is a list
            of cards.
        winner_idx (int): The index of the winning hand.

    Returns:
        int: The total score.
    """
    return sum(
        calculate_card_points(card)
        for i, hand in enumerate(hands)
        if i != winner_idx
        for card in hand
    )
