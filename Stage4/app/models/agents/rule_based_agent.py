import numpy as np
from app.models.uno.rules import is_playable

def choose_action(env, obs):
    """
    Play the first playable card in hand, otherwise draw.
    """
    hand = obs['hand']
    top_card = obs["top_card"]
    current_color = obs.get('current_color', None)

    playable = [
        card for card in hand
        if is_playable(card, top_card, current_color)
    ]
    if playable:
        # Retourne l'indice dans la liste des jouables (pour play_turn)
        return 0
    return None  # None means draw a card
