"""
constants.py

This module defines constants for a card game. It includes colors, values,
special cards, the number of cards per player.
"""

from typing import List

# Basic colors
COLORS: List[str] = ['Red', 'Green', 'Blue', 'Yellow']

# Numeric values (including 0)
VALUES: List[int] = list(range(0, 10))

# Action cards
SPECIAL_CARDS: List[str] = ['+2', 'Reverse', 'Skip']

# Wild cards – color-specific for action disambiguation
WILD_CARDS: List[str] = (
    [f"Wild {color}" for color in COLORS] +
    [f"Wild +4 {color}" for color in COLORS]
)

# Full deck
ALL_CARDS: List[str] = (
    [f"{color} {value}" for color in COLORS for value in VALUES] +
    [f"{color} {special}" for color in COLORS for special in SPECIAL_CARDS] +
    WILD_CARDS
)

# Count total distinct playable cards
NUM_CARDS: int = len(ALL_CARDS)  # Should be 108

# Wild action mapping (for agent to select color on Wild cards)
WILD_ACTIONS = {
    f"Wild {color}": NUM_CARDS + i + 1 for i, color in enumerate(COLORS)
}
WILD_ACTIONS.update({
    f"Wild +4 {color}": NUM_CARDS + i + 5 for i, color in enumerate(COLORS)
})

# Game constraints
CARDS_PER_PLAYER: int = 7
MAX_PLAYERS: int = 10
PLAYER_NAMES: List[str] = [f"Player {i}" for i in range(MAX_PLAYERS)]
