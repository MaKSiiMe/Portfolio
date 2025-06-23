"""
uno_env.py

UNO Gymnasium Environment

This module implements a custom Gymnasium environment for the UNO card game.
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Optional, Tuple, Dict

from app.models.uno.deck import create_deck
from app.models.uno.game import Game
from app.models.uno.utils import encode_hand
from app.models.uno.encodings import CARD2IDX, ALL_CARDS
from app.models.uno.rules import is_playable

NUM_CARDS = len(ALL_CARDS)
MAX_HAND_SIZE = 20  # Adjustable if necessary

def _normalize_top_card(card: str) -> str:
    """
    Normalize top card for encoding by removing color from Wild cards.
    Example: 'Green Wild +4' -> 'Wild +4'
    """
    parts = card.split()
    if parts[0] in {"Red", "Green", "Blue", "Yellow"} and "Wild" in card:
        return " ".join(parts[1:])  # Keeps 'Wild' or 'Wild +4'
    return card

class UnoEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, seed: Optional[int] = None):
        super().__init__()
        self._seed = seed
        self.rng = np.random.default_rng(seed)

        self.action_space = spaces.Discrete(NUM_CARDS + 1)  # +1 for 'draw'

        self.observation_space = spaces.Dict({
            "hand": spaces.Box(low=-1, high=NUM_CARDS, shape=(MAX_HAND_SIZE,), dtype=np.int32),
            "top_card": spaces.Discrete(NUM_CARDS),
            "opponent_card_count": spaces.Discrete(100),  # Arbitrary upper limit
        })

        self.game = None

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[Dict, Dict]:
        """
        Resets the environment and starts a new UNO game.
        """
        self.game = Game(num_players=2, seed=seed or self._seed)
        self.game.start()

        obs = self._get_obs()
        info = {}
        return obs, info

    def step(self, action: int) -> Tuple[Dict, float, bool, bool, Dict]:
        """
        Execute an action and return the environment feedback.
        """

        hand = self.game.hands[self.game.current_player]
        top_card = self.game.discard_pile[-1]
        normalized_top_card = _normalize_top_card(top_card)

        if action == NUM_CARDS:
            # Action = Draw
            self.game.draw_cards(self.game.current_player, 1)
            self.game.advance_turn()
            reward = -0.1
        else:
            card_to_play = ALL_CARDS[action]
            # Cherche tous les indices où la carte est présente et jouable
            playable_indices = [
                idx for idx, card in enumerate(hand)
                if card == card_to_play and (
                    card.startswith("Wild") or
                    card.split()[0] == top_card.split()[0] or
                    (len(card.split()) > 1 and len(top_card.split()) > 1 and card.split()[1] == top_card.split()[1])
                )
            ]
            # On vérifie que l'indice est bien valide dans la liste des cartes jouables
            if playable_indices:
                # On doit retrouver l'indice de la carte dans la liste des cartes jouables (pas juste dans la main)
                # Pour éviter ValueError dans play_turn, il faut calculer l'indice dans la liste 'playable'
                playable = [card for card in hand if (
                    card.startswith("Wild") or
                    card.split()[0] == top_card.split()[0] or
                    (len(card.split()) > 1 and len(top_card.split()) > 1 and card.split()[1] == top_card.split()[1])
                )]
                # On cherche la position de card_to_play dans la liste 'playable'
                try:
                    idx_in_playable = playable.index(card_to_play)
                    result = self.game.play_turn(human_input=idx_in_playable)
                    reward = 1.0 if result else 0.5
                except ValueError:
                    # Sécurité : la carte n'est pas dans la liste des jouables
                    self.game.draw_cards(self.game.current_player, 1)
                    self.game.advance_turn()
                    reward = -1.0
            else:
                # Invalid action → draw penalty
                self.game.draw_cards(self.game.current_player, 1)
                self.game.advance_turn()
                reward = -1.0

        done = any(len(h) == 0 for h in self.game.hands)
        truncated = False
        obs = self._get_obs()
        info = {}

        return obs, reward, done, truncated, info


    def _get_obs(self) -> Dict:
        """
        Builds the observation dictionary from the current game state.
        """
        player_hand = self.game.hands[self.game.current_player]
        top_card = self.game.discard_pile[-1]
        normalized_top_card = _normalize_top_card(top_card)

        try:
            top_card_idx = CARD2IDX[normalized_top_card]
        except KeyError:
            raise ValueError(f"Top card '{normalized_top_card}' not found in CARD2IDX")

        return {
            "hand": encode_hand(player_hand, max_size=MAX_HAND_SIZE),
            "top_card": top_card_idx,
            "opponent_card_count": len(self.game.hands[1])
        }

    def render(self):
        """
        Print the game board for visualization.
        """
        self.game.print_board()
