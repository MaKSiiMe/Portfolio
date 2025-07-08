import numpy as np
import gymnasium as gym
from gymnasium import spaces
from gymnasium.utils import seeding
from typing import Optional, Dict, Tuple

from app.models.uno.encodings import CARD2IDX
from app.models.uno.constants import COLORS, ALL_CARDS, NUM_CARDS, WILD_ACTIONS
from app.models.uno.deck import create_deck
from app.models.uno.game import Game
from app.models.uno.rules import is_playable
from app.models.uno.utils import encode_hand, decode_card

NUM_ACTIONS = NUM_CARDS + 1 + len(WILD_ACTIONS)

class UnoEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, seed: Optional[int] = None, opponent_agent_fn=None, verbose: bool = False, max_steps: int = 200):
        super().__init__()
        self._seed = seed
        self.rng = np.random.default_rng(seed)
        self.verbose = verbose
        self.done = False
        self.max_steps = max_steps
        self.action_space = spaces.Discrete(NUM_ACTIONS)

        self.observation_space = spaces.Dict({
            "hand": spaces.Box(low=0.0, high=np.inf, shape=(NUM_CARDS,), dtype=np.float32),
            "top_card": spaces.Discrete(NUM_CARDS),
            "opponent_card_count": spaces.Discrete(100),
            "current_color": spaces.MultiBinary(4),
            "draw_effect_active": spaces.Discrete(5),
            "opponent_at_uno": spaces.Discrete(2),
            "turns_without_play": spaces.Discrete(10),
        })

        self.game = None
        self.opponent_agent_fn = opponent_agent_fn

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None):
        self.done = False
        self.step_count = 0
        self._seed = seed or self._seed
        self.np_random, _ = seeding.np_random(self._seed)

        self.game = Game(num_players=2, seed=self._seed)
        if self.verbose:
            print(f"[DEBUG] Initialisation du Game avec agent_type = {self.game.agent_type}")
            print(f"[DEBUG] Agents utilisés : {self.game.agents}")
        self.game.start()
        self.game.current_player = 0

        obs = self._get_obs_player(self.game.current_player)
        return obs, {}

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        if self.done:
            winner = self.game.get_winner()
            reward = 10.0 if winner == self.game.current_player else -5.0
            obs = self._get_obs_player(self.game.current_player)
            return obs, reward, self.done, False, {}

        self.step_count += 1
        reward = 0.0
        player = self.game.current_player
        hand = self.game.hands[player]
        hand_size_before = len(hand)
        top_card = self.game.discard_pile[-1]
        current_color = self.game.current_color

        playable_cards = [
            (i, card) for i, card in enumerate(hand)
            if is_playable(card, top_card, current_color)
        ]
        has_playable = len(playable_cards) > 0

        if action == NUM_CARDS:
            reward += -1.0 if has_playable else -0.1
            self.game.draw_cards(player, 1)
            self.game.advance_turn()

        elif 0 <= action < NUM_CARDS:
            card_to_play = decode_card(action)
            found = False
            for idx, card in enumerate(hand):
                if card == card_to_play and is_playable(card, top_card, current_color):
                    try:
                        self.game.play_turn(human_input=idx)
                        reward += 0.5
                        if any(x in card for x in ["+2", "+4", "Skip", "Reverse", "Wild"]):
                            reward += 0.2
                        found = True
                        break
                    except Exception:
                        continue
            if not found:
                reward += -2.0 if has_playable else -1.0
                self.game.draw_cards(player, 1)
                self.game.advance_turn()

        elif NUM_CARDS < action < NUM_ACTIONS:
            wild_index = action - (NUM_CARDS + 1)
            if wild_index < len(WILD_ACTIONS):
                color = list(WILD_ACTIONS.keys())[wild_index].split()[-1]
                matching_card = next((card for card in hand if f"Wild" in card and color in card), None)
                if matching_card and is_playable(matching_card, top_card, current_color):
                    idx = hand.index(matching_card)
                    self.set_current_color(color)
                    self.game.play_turn(human_input=idx)
                    reward += 0.5 + 0.2
                else:
                    reward += -2.0
                    self.game.draw_cards(player, 1)
                    self.game.advance_turn()
        else:
            reward += -2.0
            self.game.draw_cards(player, 1)
            self.game.advance_turn()

        hand_size_after = len(self.game.hands[player])
        reward += (hand_size_before - hand_size_after) * 0.1

        if len(self.game.hands[1 - player]) == 1:
            reward += -1.0

        winner = self.game.get_winner()
        done = (
            winner is not None or
            any(len(h) == 0 for h in self.game.hands) or
            self.step_count >= self.max_steps
        )
        truncated = self.step_count >= self.max_steps
        self.done = done

        if done:
            if winner == player:
                reward += 10.0
            elif winner is not None:
                reward += -10.0
            else:
                reward += -5.0

        while not self.done and self.game.current_player != player:
            if self.opponent_agent_fn is not None:
                opponent = self.game.current_player
                state = self.game.get_state()
                action = self.opponent_agent_fn(self, state)
                if action == NUM_CARDS:
                    self.game.draw_cards(opponent, 1)
                    self.game.advance_turn()
                elif 0 <= action < NUM_CARDS:
                    try:
                        card = decode_card(action)
                        hand = self.game.hands[opponent]
                        for i, c in enumerate(hand):
                            if c == card and is_playable(c, self.game.discard_pile[-1], self.game.current_color):
                                self.game.play_turn(human_input=i)
                                break
                        else:
                            self.game.draw_cards(opponent, 1)
                            self.game.advance_turn()
                    except Exception:
                        self.game.draw_cards(opponent, 1)
                        self.game.advance_turn()
                else:
                    self.game.draw_cards(opponent, 1)
                    self.game.advance_turn()
            else:
                self.game.advance_turn()

            winner = self.game.get_winner()
            self.done = (
                winner is not None or
                any(len(h) == 0 for h in self.game.hands) or
                self.step_count >= self.max_steps
            )
            truncated = self.step_count >= self.max_steps

        obs = self._get_obs_player(player)
        return obs, reward, done, truncated, {}

    def _get_obs_player(self, player: int) -> Dict:
        player_hand = self.game.hands[player]
        top_card = self.game.discard_pile[-1]

        # Indice de la top_card (normalisé si besoin)
        try:
            top_card_idx = CARD2IDX[top_card]
        except KeyError:
            raise ValueError(f"Top card '{top_card}' not found in CARD2IDX")

        # One-hot encoding de la couleur active
        current_color = self.game.current_color
        color_idx = COLORS.index(current_color) if current_color in COLORS else -1
        one_hot_color = np.zeros(4, dtype=np.int8)
        if 0 <= color_idx < 4:
            one_hot_color[color_idx] = 1

        # Effets de pioche actifs (max 4 pour caper l'impact)
        draw_effect = self.game.draw_two_next * 2 + self.game.draw_four_next * 4
        draw_effect = min(draw_effect, 4)

        return {
            "hand": encode_hand(player_hand),
            "top_card": top_card_idx,
            "opponent_card_count": len(self.game.hands[1 - player]),
            "current_color": one_hot_color,
            "draw_effect_active": draw_effect,
            "opponent_at_uno": int(len(self.game.hands[1 - player]) == 1),
            "turns_without_play": min(self.step_count, 9),  # tronqué à 9 max pour rester dans l’espace défini
        }

    def render(self):
        self.game.print_board()

    def set_current_color(self, color: str) -> bool:
        if hasattr(self.game, "set_current_color"):
            return self.game.set_current_color(color)
        if color in COLORS:
            self.game.current_color = color
            return True
        return False

    def ppo_agent_fn(env, state):
        action, _ = model.predict(state, deterministic=True)
        return int(action)