# random_agent.py

from app.models.uno.rules import is_playable
from app.models.uno.encodings import CARD2IDX
from app.models.uno.utils import encode_card, TOTAL_CARDS
import numpy as np

class RandomAgent:
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)

    def __call__(self, env, obs):
        player_idx = env.game.current_player
        game_state = env.game.get_state()
        return self.choose_action(game_state, player_idx)

    def choose_action(self, game_state, player_idx):
        """
        Choisit aléatoirement une carte jouable dans la main, ou pioche si aucune.

        Args:
            game_state (dict): état brut du jeu (Game.get_state())
            player_idx (int): index du joueur courant

        Returns:
            int: action (0-107 pour jouer une carte, 108 = piocher)
        """
        hand = game_state["hands"][player_idx]
        top_card = game_state["discard_pile"][-1]
        current_color = game_state.get("current_color", None)

        playable_cards = [card for card in hand if is_playable(card, top_card, current_color)]

        if playable_cards:
            selected_card = self.rng.choice(playable_cards)
            return encode_card(selected_card)
        else:
            return TOTAL_CARDS  # Draw
