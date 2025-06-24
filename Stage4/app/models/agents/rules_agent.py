from app.models.uno.rules import is_playable
from app.models.uno.encodings import IDX2CARD, CARD2IDX

def choose_action(env, obs):
    """
    Play the first playable card in hand, otherwise draw.
    Returns an integer action index (dans ALL_CARDS), ou l'action 'draw'.
    """
    hand = [IDX2CARD[c] for c in obs['hand'] if c in IDX2CARD]
    top_card = IDX2CARD[obs["top_card"]]
    current_color = obs.get('current_color', None)

    playable = [
        card for card in hand
        if is_playable(card, top_card, current_color)
    ]
    if playable:
        return CARD2IDX[playable[0]]
    return env.action_space.n - 1
