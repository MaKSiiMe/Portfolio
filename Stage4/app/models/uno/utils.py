# utils.py

from typing import Dict, List
from .constants import COLORS, VALUES, SPECIAL_CARDS, WILD_CARDS

ALL_CARDS: List[str] = []

# Encodage/décodage des cartes
CARD_ENCODING: Dict[str, int] = {}
CARD_DECODING: Dict[int, str] = {}

_card_id = 0

# Cartes numérotées
for color in COLORS:
    ALL_CARDS.append(f"{color} 0")
    for value in VALUES:
        ALL_CARDS.append(f"{color} {value}")
    for special in SPECIAL_CARDS:
        ALL_CARDS.append(f"{color} {special}")

# Cartes spéciales sans couleur
ALL_CARDS.extend(WILD_CARDS)

# Dictionnaires d'encodage et décodage
CARD2IDX: Dict[str, int] = {card: idx for idx, card in enumerate(ALL_CARDS)}
IDX2CARD: Dict[int, str] = {idx: card for idx, card in enumerate(ALL_CARDS)}


def encode_card(card_str: str) -> int:
    """Convertit une carte en entier unique"""
    return CARD2IDX[card_str]


def decode_card(card_id: int) -> str:
    """Convertit un entier en carte"""
    return IDX2CARD[card_id]


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
    return [decode_card(idx) for idx in encoded_hand if idx != -1]