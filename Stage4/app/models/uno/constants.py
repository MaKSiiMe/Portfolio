"""
constants.py

This module defines constants for a card game. It includes colors, values,
special cards, the number of cards per player.
"""

from typing import List

COLORS: List[str] = ['Red', 'Green', 'Blue', 'Yellow']
VALUES: List[int] = list(range(1, 10))
SPECIAL_CARDS: List[str] = ['+2', 'Reverse', 'Skip']
WILD_CARDS: List[str] = ['Wild', 'Wild +4']

CARDS_PER_PLAYER: int = 7
MAX_PLAYERS: int = 10
PLAYER_NAMES = [f"Player {i}" for i in range(MAX_PLAYERS)]
