import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces

class UnoEnv(gym.Env):
    """
    Custom UNO Environment compatible with Gymnasium for Reinforcement Learning.
    """

    def __init__(self, num_players=2):
        super(UnoEnv, self).__init__()

        self.num_players = num_players
        self.current_player = 0
        self.direction = 1  # 1 = clockwise, -1 = counter-clockwise
        self.deck = self._init_deck()
        self.hands = [[] for _ in range(self.num_players)]
        self.discard_pile = []
        self.current_color = None
        self.current_value = None

        self.hand_size = 7
        self.max_cards_in_hand = 50  # used to define observation space size

        # Define action and observation spaces
        self.action_space = spaces.Discrete(self.max_cards_in_hand + 1)  # play a card (0 to n-1) or draw (n)
        self.observation_space = spaces.Dict({
            "hand": spaces.MultiDiscrete([108] * self.max_cards_in_hand),  # index in deck, padded with -1
            "top_card": spaces.Discrete(108),
            "hand_lengths": spaces.MultiDiscrete([self.max_cards_in_hand + 1] * self.num_players),
            "current_player": spaces.Discrete(self.num_players),
        })

    def _init_deck(self):
        # Simplified deck representation: 108 cards
        deck = list(range(108))
        random.shuffle(deck)
        return deck

    def _deal_cards(self):
        for player in range(self.num_players):
            self.hands[player] = [self.deck.pop() for _ in range(self.hand_size)]

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.deck = self._init_deck()
        self._deal_cards()

        self.discard_pile = [self.deck.pop()]
        self.current_color = self._get_card_color(self.discard_pile[-1])
        self.current_value = self._get_card_value(self.discard_pile[-1])
        self.current_player = 0
        self.direction = 1

        return self._get_obs(), {}

    def _get_obs(self):
        hand = self.hands[self.current_player]
        padded_hand = hand + [-1] * (self.max_cards_in_hand - len(hand))

        return {
            "hand": np.array(padded_hand, dtype=np.int32),
            "top_card": int(self.discard_pile[-1]),
            "hand_lengths": np.array([len(h) for h in self.hands], dtype=np.int32),
            "current_player": self.current_player,
        }

    def _get_card_color(self, card_id):
        # Dummy placeholder: card color = card_id % 4
        return card_id % 4

    def _get_card_value(self, card_id):
        # Dummy placeholder: card value = card_id % 10
        return card_id % 10

    def step(self, action):
        # Placeholder logic for playing or drawing a card
        reward = 0
        done = False
        info = {}

        hand = self.hands[self.current_player]

        if action < len(hand):
            played_card = hand.pop(action)
            self.discard_pile.append(played_card)
            self.current_color = self._get_card_color(played_card)
            self.current_value = self._get_card_value(played_card)

            if len(hand) == 0:
                reward = 1
                done = True
        else:
            if len(self.deck) > 0:
                hand.append(self.deck.pop())

        self.current_player = (self.current_player + self.direction) % self.num_players
        return self._get_obs(), reward, done, False, info

    def render(self):
        print(f"Player {self.current_player}'s turn")
        print("Hand:", self.hands[self.current_player])
        print("Top card:", self.discard_pile[-1])
        print("Hand sizes:", [len(h) for h in self.hands])


if __name__ == "__main__":
    env = UnoEnv(num_players=2)

    obs, info = env.reset()
    done = False

    step_count = 0
    while not done and step_count < 50:
        env.render()

        # Action aléatoire : jouer une carte ou piocher
        action = env.action_space.sample()
        obs, reward, done, truncated, info = env.step(action)
        step_count += 1

        print(f"Action: {action}, Reward: {reward}, Done: {done}\n")

    print("Episode finished.")
