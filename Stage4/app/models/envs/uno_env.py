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
MAX_HAND_SIZE = 20

def _normalize_top_card(card: str) -> str:
    """
    Normalize top card for encoding by removing color from Wild cards.
    Example: 'Green Wild +4' -> 'Wild +4'
    """
    parts = card.split()
    if parts[0] in {"Red", "Green", "Blue", "Yellow"} and "Wild" in card:
        return " ".join(parts[1:])
    return card

class UnoEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, seed: Optional[int] = None, opponent_agent_fn=None):
        super().__init__()
        self._seed = seed
        self.rng = np.random.default_rng(seed)

        self.action_space = spaces.Discrete(NUM_CARDS + 1)

        self.observation_space = spaces.Dict({
            "hand": spaces.Box(low=-1, high=NUM_CARDS, shape=(MAX_HAND_SIZE,), dtype=np.int32),
            "top_card": spaces.Discrete(NUM_CARDS),
            "opponent_card_count": spaces.Discrete(100),
        })

        self.game = None
        self.opponent_agent_fn = opponent_agent_fn

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[Dict, Dict]:
        self.game = Game(num_players=2, seed=seed or self._seed)
        self.game.start()
        obs = self._get_obs()
        return obs, {}

    def step(self, action: int) -> Tuple[Dict, float, bool, bool, Dict]:
        reward = 0.0
        player = self.game.current_player
        hand = self.game.hands[player]
        top_card = self.game.discard_pile[-1]
        current_color = self.game.current_color

        # Liste des cartes jouables
        playable_cards = [
            (i, card) for i, card in enumerate(hand)
            if is_playable(card, top_card, current_color)
        ]
        has_playable = len(playable_cards) > 0

        if action == NUM_CARDS:
            if has_playable:
                reward = -2.0  # Mauvais choix, alors qu'une carte était jouable
            else:
                reward = -0.1  # Petite pénalité pour draw légitime
            self.game.draw_cards(player, 1)
            self.game.advance_turn()
        elif 0 <= action < NUM_CARDS:
            card_to_play = ALL_CARDS[action]
            matching_indices = [
                i for i, card in enumerate(hand)
                if card == card_to_play and is_playable(card, top_card, current_color)
            ]
            if matching_indices:
                try:
                    idx = matching_indices[0]
                    result = self.game.play_turn(human_input=idx)
                    reward = 1.0 if result else 0.5
                except Exception:
                    reward = -1.0
                    self.game.draw_cards(player, 1)
                    self.game.advance_turn()
            else:
                reward = -2.0 if has_playable else -1.0
                self.game.draw_cards(player, 1)
                self.game.advance_turn()
        else:
            reward = -2.0  # Action invalide
            self.game.draw_cards(player, 1)
            self.game.advance_turn()

        done = any(len(h) == 0 for h in self.game.hands)
        truncated = False

        # Adversaire automatique
        while not done and self.game.current_player != player:
            if self.opponent_agent_fn is not None:
                obs_opponent = self._get_obs_player(self.game.current_player)
                opponent_action = self.opponent_agent_fn(self, obs_opponent)

                opponent = self.game.current_player
                hand = self.game.hands[opponent]
                top_card = self.game.discard_pile[-1]
                current_color = self.game.current_color

                card_to_play = (
                    ALL_CARDS[opponent_action]
                    if opponent_action is not None and 0 <= opponent_action < NUM_CARDS
                    else None
                )

                playable = [
                    idx for idx, card in enumerate(hand)
                    if card == card_to_play and is_playable(card, top_card, current_color)
                ]

                if card_to_play and playable:
                    try:
                        idx_in_hand = playable[0]
                        self.game.play_turn(human_input=idx_in_hand)
                    except Exception:
                        self.game.draw_cards(opponent, 1)
                        self.game.advance_turn()
                else:
                    self.game.draw_cards(opponent, 1)
                    self.game.advance_turn()

                done = any(len(h) == 0 for h in self.game.hands)
            else:
                self.game.advance_turn()

        obs = self._get_obs()
        return obs, reward, done, truncated, {}

    def _get_obs(self) -> Dict:
        return self._get_obs_player(self.game.current_player)

    def _get_obs_player(self, player: int) -> Dict:
        player_hand = self.game.hands[player]
        top_card = self.game.discard_pile[-1]
        normalized_top_card = _normalize_top_card(top_card)

        try:
            top_card_idx = CARD2IDX[normalized_top_card]
        except KeyError:
            raise ValueError(f"Top card '{normalized_top_card}' not found in CARD2IDX")

        return {
            "hand": encode_hand(player_hand, max_size=MAX_HAND_SIZE),
            "top_card": top_card_idx,
            "opponent_card_count": len(self.game.hands[1 - player])
        }

    def render(self):
        self.game.print_board()
