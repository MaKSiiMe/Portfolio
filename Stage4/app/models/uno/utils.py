# utils.py

from typing import Dict, List
from .constants import COLORS, VALUES, SPECIAL_CARDS, WILD_CARDS

# Encodage/décodage des cartes
CARD_ENCODING: Dict[str, int] = {}
CARD_DECODING: Dict[int, str] = {}

_card_id = 0

# Cartes "0" (une seule par couleur)
for color in COLORS:
    card = f"{color} 0"
    CARD_ENCODING[card] = _card_id
    CARD_DECODING[_card_id] = card
    _card_id += 1

# Cartes numérotées 1-9 (deux par couleur)
for color in COLORS:
    for value in VALUES:
        card = f"{color} {value}"
        for _ in range(2):
            CARD_ENCODING[card] = _card_id
            CARD_DECODING[_card_id] = card
            _card_id += 1

# Cartes spéciales couleur (deux par couleur)
for color in COLORS:
    for special in SPECIAL_CARDS:
        card = f"{color} {special}"
        for _ in range(2):
            CARD_ENCODING[card] = _card_id
            CARD_DECODING[_card_id] = card
            _card_id += 1

# Cartes Wild (4 exemplaires)
for wild in WILD_CARDS:
    for _ in range(4):
        CARD_ENCODING[wild] = _card_id
        CARD_DECODING[_card_id] = wild
        _card_id += 1

TOTAL_CARDS = _card_id  # = 108


def encode_card(card_str: str) -> int:
    """Convertit une carte en entier unique"""
    return CARD_ENCODING[card_str]


def decode_card(card_id: int) -> str:
    """Convertit un entier en carte"""
    return CARD_DECODING[card_id]


def encode_hand(hand: List[str], max_size: int = 20) -> List[int]:
    """
    Encode une main de cartes en liste d'entiers, avec padding -1.

    Args:
        hand (List[str]): Liste des cartes (str)
        max_size (int): Longueur max (ex: 20)

    Returns:
        List[int]: Liste d'entiers de taille fixe
    """
    encoded = [encode_card(card) for card in hand]
    padded = encoded + [-1] * (max_size - len(encoded))
    return padded[:max_size]


def decode_hand(encoded_hand: List[int]) -> List[str]:
    """
    Convertit une liste d'entiers en noms de cartes (str), ignore les -1.

    Args:
        encoded_hand (List[int]): Entiers

    Returns:
        List[str]: Cartes correspondantes
    """
    return [decode_card(cid) for cid in encoded_hand if cid != -1]
