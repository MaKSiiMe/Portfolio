"""
deck.py

This module provides functionalities to create and manage a deck of cards
for the UNO game.

Functions:
- create_deck: Generates a shuffled deck of cards.
- reshuffle_discard_pile: Reshuffles the discard pile into the deck when
  the deck is empty.
"""

import random
import time
from typing import List, Optional
from .constants import COLORS, VALUES, SPECIAL_CARDS, WILD_CARDS


def create_deck(seed: Optional[int] = None) -> List[str]:
    """
    Generates a shuffled deck of UNO cards.

    Args:
        seed (Optional[int]): Seed for random number generator.
            If None, uses current time.

    Returns:
        List[str]: A list representing the shuffled deck of cards.
    """
    deck = []
    for color in COLORS:
        deck.append(f"{color} 0")
        for value in VALUES:
            deck.extend([f"{color} {value}"] * 2)
        for special in SPECIAL_CARDS:
            deck.extend([f"{color} {special}"] * 2)
    for card in WILD_CARDS:
        deck.extend([card] * 4)

    random.seed(seed if seed is not None else time.time())
    random.shuffle(deck)
    return deck


def reshuffle_discard_pile(deck: List[str], discard_pile: List[str]) -> None:
    """
    Reshuffles the discard pile into the deck when the deck is empty.

    Args:
        deck (List[str]): The current deck of cards.
        discard_pile (List[str]): The current discard pile.

    Returns:
        None
    """
    if len(discard_pile) <= 1:
        return

    top_card = discard_pile.pop()
    random.shuffle(discard_pile)
    deck.extend(discard_pile)
    discard_pile.clear()
    discard_pile.append(top_card)
    print(
        "La pioche était vide : la défausse a été mélangée pour former une "
        "nouvelle pioche."
    )
