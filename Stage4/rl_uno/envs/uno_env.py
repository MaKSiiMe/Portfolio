"""
uno_env.py

UNO Gymnasium Environment

This module implements a custom Gymnasium environment for the UNO card game.
It wraps the core UNO engine to provide observations, actions, rewards, and environment dynamics for training AI agents.
"""

import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import List, Tuple, Dict, Optional

from uno.deck import create_deck
from uno.constants import MAX_PLAYERS, CARDS_PER_PLAYER, MAX_HAND_SIZE
from uno.utils import ALL_CARDS, CARD2IDX, IDX2CARD, encode_hand


class UnoEnv(gym.Env):

    metadata = {"render_modes": ["human"]}

    def __init__(self, num_players: int = 2, seed: Optional[int] = None):
        super().__init__()
        assert 2 <= num_players <= MAX_PLAYERS, f"Number of players must be between 2 and {MAX_PLAYERS}."
        self.num_players = num_players
        self._seed = seed

        # Observation space: hand of the agent + top card of discard pile + count of opponent's cards
        self.observation_space = spaces.Dict({
            "hand": spaces.Box(low=-1, high=NUM_CARDS, shape=(MAX_HAND_SIZE,), dtype=np.int),
            "top_card": spaces.Discrete(NUM_CARDS),
            "opponent_card_count": spaces.Discrete(NUM_CARDS)
        })

        # Action space: one action per card + one action to draw a card
        self.action_space = spaces.Discrete(NUM_CARDS + 1)

        # Internal game state
        self.deck: List[str] = []
        self.hands: List[List[str]] = []
        self.discard_pile: List[str] = []
        self.current_player: int = 0

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[Dict, Dict]:
        self.deck = create_deck(seed=self.seed)
        self hands = [[self.deck.pop() for _ in range(CARDS_PER_PLAYER)] for _ in range(self.num_players)]
        self.discard_pile = [self.deck.pop()]
        self.current_player = 0

        obs = self._get_observation()
        info = {}
        return obs, info {}

    def step(self, action int) -> Tuple[Dict, float, bool, bool, Dict]:

        player_hand = self.hands[self.current_player]
        top_card = self.discard_pile[-1]

        if action == NUM_CARDS:  # Draw a card
            if self.deck:
                player_hand.append(self.deck.pop())
            reward = -0.1
        else:
            try:
                card_to_play = IDX2CARD[action]
            exept KeyError:
                card_to_play = None
            if card_to_play in player_hand and self._is_playble(card_to_play, top_card):
                player_hand.remove(card_to_play)
                self.discard_pile.append(card_to_play)
                reward = 1.0 if not player_hand else 0.5
            else:
                card_to_play = None
                reward = -1.0

        terminal = len(player_hand) == 0
        truncated = False  # No max step for now

        obs = self._get_observation()
        info = {}

        # exemple d'appel fictif :
        self.game.play_turn(action)

        if self.game.is_over():
            done = True
            reward = self._get_reward()

        obs = self._get_obs()
        return obs, reward, done, truncated, info

    def render(self):
        print(f"Player {self.current_player} hand: {self.hands[self.current_player]}")
        print(f"Top card: {self.discard_pile[-1]}")
        print(f"Opponent card count: {len(self.hands[1 - self.current_player])}")

    def _get_observation(self) -> Dict:
        return {
            "hand": ecode_hand(self.hands[self.current_player], max_size=MAX_HAND_SIZE),
            "top_card": CARD2IDX[self.discard_pile[-1]],
            "opponent_card_count": len(self.hands[1 - self.current_player])
        }

    def _is_playable(self, card: str, top_card: str) -> bool:
        if card i n ["Wild", "Wild +4"]:
            return True
        card_color, *card_value = card.split()
        top_color, *top_value = top_card.split()
        return card_color == top_color or card_value == top_value
