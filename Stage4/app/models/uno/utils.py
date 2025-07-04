from typing import Dict, List
from .constants import COLORS, VALUES, SPECIAL_CARDS, WILD_CARDS

ALL_CARDS = []
for color in COLORS:
    ALL_CARDS.append(f"{color} 0")
    for value in VALUES:
        ALL_CARDS.append(f"{color} {value}")
    for special in SPECIAL_CARDS:
        ALL_CARDS.append(f"{color} {special}")
ALL_CARDS.extend(WILD_CARDS)

CARD2IDX: Dict[str, int] = {card: idx for idx, card in enumerate(ALL_CARDS)}
IDX2CARD: Dict[int, str] = {idx: card for idx, card in enumerate(ALL_CARDS)}

TOTAL_CARDS = len(ALL_CARDS)  # Nombre total de cartes dans le jeu
import numpy as np

def encode_card(card_str: str) -> int:
    """Convertit une carte en entier unique"""
    return CARD2IDX[card_str]

def decode_card(card_id: int) -> str:
    """Convertit un entier en carte"""
    return IDX2CARD[card_id]

def encode_hand(hand: List[str]) -> np.ndarray:
    """
    Encode une main de cartes en vecteur de fréquences (longueur = TOTAL_CARDS)
    """
    vec = np.zeros(len(CARD2IDX), dtype=np.float32)
    for card in hand:
        vec[CARD2IDX[card]] += 1
    return vec

def decode_hand(encoded_hand: List[int]) -> List[str]:
    """
    Convertit une liste d'entiers en noms de cartes (str), ignore les -1.
    """
    return [decode_card(cid) for cid in encoded_hand if cid != -1]
