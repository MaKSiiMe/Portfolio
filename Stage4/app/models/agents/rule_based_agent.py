import numpy as np
from app.models.uno.rules import is_playable
from app.models.uno.encodings import IDX2CARD, ALL_CARDS

def choose_action(env, obs):
    """
    Play the first playable card in hand, otherwise draw.
    """
    hand = obs['hand']
    top_card = IDX2CARD[obs["top_card"]]
    current_color = obs['current_color']

    for idx, card in enumerate(hand):
        if is_playable(card, top_card, current_color):
            return idx  # index in hand for play_turn(human_input=idx)
    return None  # None means draw a card
    
    # Last index reserved for 'draw card'
    return env.action_space.n - 1
