"""
rules.py

This module contains functions to determine the playability of cards and
calculate scores in a UNO game.
"""

from typing import List


def is_playable(card: str, top_card: str, current_color: str) -> bool:
    """
    Determine if a card is playable based on the current color or the top card.

    Args:
        card (str): The card to check.
        top_card (str): The top card of the discard pile.
        current_color (str): The active color in play.

    Returns:
        bool: True if the card is playable, False otherwise.
    """
    card_parts = card.split()
    top_parts = top_card.split()

    if not card_parts or not top_parts:
        return False

    if card_parts[0] == 'Wild':
        return True

    card_color = card_parts[0]
    card_value = " ".join(card_parts[1:]) if len(card_parts) > 1 else None

    top_color = top_parts[0]
    top_value = " ".join(top_parts[1:]) if len(top_parts) > 1 else None

    return card_color == current_color or card_value == top_value

def get_playable_cards(hand: List[str], top_card: str, current_color: str) -> List[str]:
    """
    Get a list of playable cards from a hand based on the top card and current color.

    Args:
        hand (List[str]): The player's hand of cards.
        top_card (str): The top card of the discard pile.
        current_color (str): The active color in play.

    Returns:
        List[str]: A list of playable cards.
    """
    return [
        card for card in hand
        if is_playable(card, top_card, current_color)
    ]

def get_playable_cards_with_indices(hand: List[str], top_card: str, current_color: str) -> List[int]:
    """
    Get indices of playable cards from a hand based on the top card and current color.

    Args:
        hand (List[str]): The player's hand of cards.
        top_card (str): The top card of the discard pile.
        current_color (str): The active color in play.

    Returns:
        List[int]: A list of indices of playable cards.
    """
    return [
        i for i, card in enumerate(hand)
        if is_playable(card, top_card, current_color)
    ]

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
