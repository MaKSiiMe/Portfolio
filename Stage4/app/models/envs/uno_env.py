"""
uno_env.py

UNO Gymnasium Environment

This module implements a custom Gymnasium environment for the UNO card game.
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np

from app.models.uno.deck import create_deck, reshuffle_discard_pile  

class UnoEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self):
        super().__init__()
        
        # Action: jouer une carte parmi 108 (max deck size), ou passer/piocher (on encode tout dans 1 Discrete)
        self.action_space = spaces.Discrete(109)

        # Observation: à définir proprement — ici on part sur une observation flat de taille fixe
        self.observation_space = spaces.Dict({
            "hand": spaces.Box(0, 108, shape=(7,), dtype=np.int32),
            "top_card": spaces.Discrete(108),
            "opponent_card_count": spaces.Discrete(108),
            # d'autres flags ou encodages possibles ici
        })

        self.game = None  # ton moteur UNO ici

    def reset(self, seed=None, options=None):
        # Initialise une nouvelle partie
        self.game = UnoGame(num_players=2)
        self.game.start_new_game()

        obs = self._get_obs()
        return obs, {}

    def step(self, action):
        # Appliquer l'action dans ton moteur
        # Attention à bien gérer : validité de l'action, tour du joueur, effets spéciaux, etc.

        reward = 0
        done = False
        truncated = False

        info = {}

        # exemple d'appel fictif :
        self.game.play_turn(action)

        if self.game.is_over():
            done = True
            reward = self._get_reward()

        obs = self._get_obs()
        return obs, reward, done, truncated, info

    def _get_obs(self):
        # Encode la main de l'agent, la carte du dessus, etc.
        # Tu peux ici transformer ton état du moteur UNO en format NumPy/Gym
        return {
            "hand": np.array([...]),
            "top_card": ...,
            "opponent_card_count": ...
        }

    def _get_reward(self):
        # Exemple naïf :
        if self.game.winner == 0:
            return 1
        else:
            return -1

    def render(self):
        self.game.print_state()
