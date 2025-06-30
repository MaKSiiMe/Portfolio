"""
uno_env.py

UNO Gymnasium Environment

This module implements a custom Gymnasium environment for the UNO card game.
"""

import gymnasium as gym
from gymnasium import spaces
from gymnasium.utils import seeding
import numpy as np
from typing import Optional, Tuple, Dict

from app.models.uno.deck import create_deck
from app.models.uno.game import Game
from app.models.uno.utils import encode_hand, encode_state, decode_card, normalize_top_card
from app.models.uno.encodings import CARD2IDX, ALL_CARDS
from app.models.uno.rules import is_playable

NUM_CARDS = len(ALL_CARDS)
MAX_HAND_SIZE = 20
TOTAL_CARDS = NUM_CARDS


class UnoEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, seed: Optional[int] = None, opponent_agent_fn=None, verbose: bool = False):
        super().__init__()
        self._seed = seed
        self.rng = np.random.default_rng(seed)
        self.verbose = verbose
        self.done = False

        self.action_space = spaces.Discrete(NUM_CARDS + 1)

        self.observation_space = spaces.Dict({
            "hand": spaces.Box(low=0.0, high=np.inf, shape=(len(ALL_CARDS),), dtype=np.float32),
            "top_card": spaces.Discrete(len(ALL_CARDS)),
            "opponent_card_count": spaces.Discrete(100),
        })

        self.game = None
        self.opponent_agent_fn = opponent_agent_fn

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None):
        self.done = False
        self._seed = seed or self._seed
        self.np_random, _ = seeding.np_random(self._seed)

        self.game = Game(num_players=2, seed=self._seed)
        self.game.start()

        obs = self._get_obs_player(self.game.current_player)
        return obs, {}

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        if self.done:
            winner = self.game.get_winner()
            reward = [-1000.0] * len(self.game.agents)
            if winner is not None:
                reward[winner] = 1.0
            obs = encode_state(self.game.get_state(), self.game.current_player)
            return obs, reward, self.done, False, {}

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

        if action == TOTAL_CARDS:
            reward = -2.0 if has_playable else -0.1
            self.game.draw_cards(player, 1)
            self.game.advance_turn()
        elif 0 <= action < TOTAL_CARDS:
            try:
                card_to_play = decode_card(action)
                if self.verbose:
                    print(f"[RuleBased] tries to play: {card_to_play} | top: {top_card} | color: {current_color}")
            except Exception:
                card_to_play = None

            found = False
            for idx, card in enumerate(hand):
                if card_to_play and card == card_to_play and is_playable(card, top_card, current_color):
                    try:
                        result = self.game.play_turn(human_input=idx)
                        reward = 1.0 if result else 0.5
                        found = True
                        break
                    except Exception as e:
                        if self.verbose:
                            print(f"[Play failed] {e}")
                        continue

            if not found:
                reward = -2.0 if has_playable else -1.0
                self.game.draw_cards(player, 1)
                self.game.advance_turn()
        else:
            reward = -2.0
            self.game.draw_cards(player, 1)
            self.game.advance_turn()

        # Vérifie si la partie est terminée
        state = self.game.get_state()
        if state.get("winner") is not None or any(len(h) == 0 for h in self.game.hands):
            self.done = True
            if self.verbose:
                print(f"[🏁] Player {self.game.get_winner()} wins!")
        done = self.done
        truncated = False

        while not done and self.game.current_player != player:
            if self.opponent_agent_fn is not None:
                opponent = self.game.current_player
                state = self.game.get_state()
                action = self.opponent_agent_fn(self, state)
                self.step(action)
                self.done = self.game.get_winner() is not None
                done = self.done
            else:
                self.game.advance_turn()
                self.done = self.game.get_winner() is not None
                done = self.done

        obs = self._get_obs_player(player)
        return obs, reward, done, truncated, {}

    def _get_obs(self) -> Dict:
        return encode_state(self.game.get_state(), self.game.current_player)

    def _get_obs_player(self, player: int) -> Dict:
        player_hand = self.game.hands[player]
        top_card = self.game.discard_pile[-1]
        normalized_top_card = normalize_top_card(top_card)

        try:
            top_card_idx = CARD2IDX[normalized_top_card]
        except KeyError:
            raise ValueError(f"Top card '{normalized_top_card}' not found in CARD2IDX")

        return {
            "hand": encode_hand(player_hand),
            "top_card": top_card_idx,
            "opponent_card_count": len(self.game.hands[1 - player])
        }

    def render(self):
        self.game.print_board()
