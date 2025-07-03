"""
constants.py

This module defines constants for a card game. It includes colors, values,
special cards, the number of cards per player.
"""

COLORS = ["red", "green", "blue", "yellow"]
VALUES = [str(n) for n in range(10)] + [str(n) for n in range(1, 10)] + ["+2", "+2", "reverse", "reverse", "skip", "skip"]
SPECIAL_CARDS = ["+4", "wild", "+4", "wild"]

# Construction de toutes les cartes colorées
COLOR_CARDS = [{"color": color, "value": value} for color in COLORS for value in VALUES]

# Construction des cartes noires
WILD_CARDS = [{"color": "black", "value": val} for val in SPECIAL_CARDS]

# Toutes les cartes du jeu
ALL_CARDS = COLOR_CARDS + WILD_CARDS

# Nombre total de cartes
NUM_CARDS = len(ALL_CARDS)

# 💥 LA LIGNE QUI MANQUAIT
CARDS_PER_PLAYER = 7

