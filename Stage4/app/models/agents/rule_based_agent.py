import numpy as np
from app.models.uno.utils import is_playable
from app.models.uno.encodings import IDX2CARD, ALL_CARDS

def choose_action(env, obs):
    """
    Plays the first playable card if available, otherwise draws a card.
    """
    top_card = IDX2CARD[obs["top_card"]]
    playable_indices = [
        idx for idx, card in enumerate(ALL_CARDS)
        if is_playable(card, top_card)
    ]

    if playable_indices:
        return np.random.choice(playable_indices)
    
    # Last index reserved for 'draw card'
    return env.action_space.n - 1
