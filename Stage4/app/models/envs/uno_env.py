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
from app.models.uno.utils import encode_hand, encode_state, decode_card  # Ajoute decode_card à l'import
from app.models.uno.encodings import CARD2IDX, ALL_CARDS
from app.models.uno.rules import is_playable

NUM_CARDS = len(ALL_CARDS)
MAX_HAND_SIZE = 20
TOTAL_CARDS = NUM_CARDS  # Ajout pour compatibilité avec le code plus bas

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

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[np.ndarray, Dict]:
        """
        Réinitialise l'environnement pour un nouvel épisode de jeu.

        Args:
            seed (Optional[int]): Graine aléatoire
            options (Optional[Dict]): Options supplémentaires (non utilisé ici)

        Returns:
            Tuple[np.ndarray, Dict]: Observation initiale + info (vide)
        """
        self.done = False
        self._seed = seed or self._seed
        self.rng = np.random.default_rng(self._seed)
        self.game = Game(num_players=2, seed=self._seed)
        self.game.start()

        obs = encode_state(self.game.get_state(), self.game.current_player)
        return obs, {}

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """
        Applique l'action de l'agent et retourne la nouvelle observation, récompense, etc.
        """
        reward = 0.0
        player = self.game.current_player
        hand = self.game.hands[player]
        top_card = self.game.discard_pile[-1]
        current_color = self.game.current_color

        if self.done:
            winner = self.game.get_state().get("winner")
            if winner is not None:
                rewards = [-1.0] * self.game.num_players
                rewards[winner] = 1.0
            else:
                rewards = [0.0] * self.game.num_players

        # Liste des cartes jouables
        playable_cards = [
            (i, card) for i, card in enumerate(hand)
            if is_playable(card, top_card, current_color)
        ]
        has_playable = len(playable_cards) > 0

        # Action = piocher
        if action == TOTAL_CARDS:
            if has_playable:
                reward = -2.0  # Mauvais choix
            else:
                reward = -0.1  # Légère pénalité
            self.game.draw_cards(player, 1)
            self.game.advance_turn()

        # Action = jouer une carte spécifique
        elif 0 <= action < TOTAL_CARDS:
            try:
                card_to_play = decode_card(action)
                print(f"[DEBUG] RuleBased tries to play: {card_to_play}")
                print(f"[DEBUG] Top card: {top_card} | Current color: {current_color}")
                print(f"[DEBUG] Full hand: {hand}")

                if verbose:
                    print(f"RuleBased plays: {card_to_play} | top: {top_card} | color: {current_color}")
                    print(f"Hand before: {hand}")

            except Exception:
                card_to_play = None

            found = False
            for idx, card in enumerate(hand):
                if (
                    card_to_play is not None
                    and card == card_to_play
                    and is_playable(card, top_card, current_color)
                ):
                    try:
                        print(f"RuleBased plays: {card_to_play} | top: {top_card} | color: {current_color}")
                        result = self.game.play_turn(human_input=idx)
                        reward = 1.0 if result else 0.5
                        found = True
                        break
                    except Exception as e:
                        print(f"Play failed: {e}")
                        continue

            if not found:
                reward = -2.0 if has_playable else -1.0
                self.game.draw_cards(player, 1)
                self.game.advance_turn()

        # Action invalide
        else:
            reward = -2.0
            self.game.draw_cards(player, 1)
            self.game.advance_turn()

        # Vérifie si la partie est finie
        state = self.game.get_state()
        if state.get("winner") is not None or any(len(h) == 0 for h in self.game.hands):
            self.done = True
        done = self.done
        truncated = False

        # Fait jouer l'adversaire si partie non terminée
        while not done and self.game.current_player != player:
            # Correction : ne fait jouer l'adversaire que si self.opponent_agent_fn est défini
            if self.opponent_agent_fn is not None:
                opponent = self.game.current_player
                state = self.game.get_state()
                action = self.opponent_agent_fn(state, opponent)
                self.step(action)
                done = any(len(h) == 0 for h in self.game.hands)
            else:
                # Si aucun agent adversaire n'est défini, passe simplement le tour
                self.game.advance_turn()
                done = any(len(h) == 0 for h in self.game.hands)

        obs = encode_state(self.game.get_state(), player)
        return obs, reward, done, truncated, {}


    def _get_obs(self) -> Dict:
        return encode_state(self.game.get_state(), self.game.current_player)

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
