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

import numpy as np

def encode_card(card_str: str) -> int:
    """Convertit une carte en entier unique"""
    return CARD_ENCODING[card_str]


def decode_card(card_id: int) -> str:
    """Convertit un entier en carte"""
    return CARD_DECODING[card_id]


def encode_hand(hand: List[str]) -> np.ndarray:
    """
    Encode une main de cartes en vecteur de fréquences (longueur = TOTAL_CARDS)

    Args:
        hand (List[str]): Liste des cartes

    Returns:
        np.ndarray: Vecteur de fréquences (float32)
    """
    vec = np.zeros(TOTAL_CARDS, dtype=np.float32)
    for card in hand:
        vec[encode_card(card)] += 1
    return vec


def decode_hand(encoded_hand: List[int]) -> List[str]:
    """
    Convertit une liste d'entiers en noms de cartes (str), ignore les -1.

    Args:
        encoded_hand (List[int]): Entiers

    Returns:
        List[str]: Cartes correspondantes
    """
    return [decode_card(cid) for cid in encoded_hand if cid != -1]


def encode_state(game_state: dict, player_idx: int) -> np.ndarray:
    """
    Encode l'état du jeu pour un joueur donné.

    Args:
        game_state (dict): état brut du jeu (format retourné par Game.get_state())
        player_idx (int): index du joueur courant

    Returns:
        np.ndarray: vecteur représentant l'état
    """
    from .utils import encode_card, encode_hand, TOTAL_CARDS

    # Main du joueur
    hand = game_state["hands"][player_idx]
    hand_vec = encode_hand(hand)  # (108,)

    # Correction : déduire la top_card depuis discard_pile si non présente
    if "top_card" in game_state:
        top_card = game_state["top_card"]
    elif "discard_pile" in game_state and game_state["discard_pile"]:
        top_card = game_state["discard_pile"][-1]
    else:
        top_card = None

    top_card_vec = np.zeros(TOTAL_CARDS, dtype=np.float32)
    if top_card is not None:
        try:
            top_card_id = encode_card(top_card)
            top_card_vec[top_card_id] = 1.0  # One-hot
        except Exception:
            pass

    # Nombre de cartes restantes pour chaque joueur
    num_players = len(game_state["hands"])
    opponents_sizes = [
        len(game_state["hands"][i]) if i != player_idx else 0
        for i in range(num_players)
    ]
    opponents_vec = np.array(opponents_sizes, dtype=np.float32)

    # Concaténation finale
    state_vector = np.concatenate([hand_vec, top_card_vec, opponents_vec])

    return state_vector


def decode_action(index: int) -> str:
    """
    Convertit un index d'action en nom de carte, ou 'DRAW' si c'est l'action piocher.

    Args:
        index (int): index d'action

    Returns:
        str: carte jouée ou 'DRAW'
    """
    if index == TOTAL_CARDS:
        return "DRAW"
    return decode_card(index)
