from typing import List, Optional
import random
import time
import logging

from app.models.uno.constants import (
    COLORS, VALUES, SPECIAL_CARDS, WILD_CARDS, CARDS_PER_PLAYER
)
from app.models.uno.deck import create_deck, reshuffle_discard_pile
from app.models.uno.rules import is_playable, calculate_score

from app.models.agents.rules_agent import RuleBasedAgent
# from app.models.agents.random_agent import RandomAgent
# from app.models.agents.ppo_agent import PPOAgent

class Game:
    def __init__(self, num_players: int = 2, seed: Optional[int] = None, agent_type: str = "rulesbased", agents=None):
        self.num_players = num_players
        self.seed = seed
        self.agent_type = agent_type
        self.deck = create_deck(seed)
        self.hands: List[List[str]] = [[] for _ in range(num_players)]
        self.discard_pile: List[str] = []
        self.current_player = 0
        self.direction = 1
        self.draw_two_next = 0
        self.draw_four_next = 0
        self.skip_next = False
        self.skip_current_player = False
        self.consecutive_passes = 0
        self.turn = 0
        self.current_color = None
        
        if agents is not None:
            self.agents = agents
        else:
            self.agents = [None]
            for _ in range(1, num_players):
                self.agents.append(RuleBasedAgent())

    def start(self):
        for i in range(self.num_players):
            self.hands[i] = [self.deck.pop() for _ in range(CARDS_PER_PLAYER)]
        first_card = self.deck.pop()
        self.discard_pile.append(first_card)

        if first_card.startswith("Wild"):
            self.current_color = random.choice(COLORS)
            if "+4" in first_card:
                self.draw_four_next = 1
        else:
            self.current_color = first_card.split()[0]

    def handle_first_card(self):
        if self.discard_pile[-1].startswith("Wild"):
            new_color = random.choice(COLORS)
            if "+4" in self.discard_pile[-1]:
                self.discard_pile[-1] = f"{new_color} Wild +4"
                self.draw_four_next = 1
            else:
                self.discard_pile[-1] = f"{new_color} Wild"

    def get_state(self) -> dict:
        return {
            "num_players": self.num_players,
            "deck_size": len(self.deck),
            "discard_pile": self.discard_pile,
            "hands": self.hands,
            "current_player": self.current_player,
            "current_color": self.current_color,
            "direction": self.direction,
            "turn": self.turn,
            "cards_left": [len(h) for h in self.hands],
            "winner": self.get_winner(),
        }

    def draw_cards(self, player_idx: int, count: int) -> int:
        drawn = 0
        for _ in range(count):
            if not self.deck:
                reshuffle_discard_pile(self.deck, self.discard_pile)
            if self.deck:
                self.hands[player_idx].append(self.deck.pop())
                drawn += 1
        return drawn

    def play_turn(self, human_input: Optional[int] = None) -> Optional[int]:
        player = self.current_player
        hand = self.hands[player]
        top_card = self.discard_pile[-1]

        if not hand:
            return player

        # Effets spéciaux accumulés à appliquer AVANT le tour
        if self.draw_four_next:
            self.draw_cards(player, 4 * self.draw_four_next)
            self.draw_four_next = 0
            self.skip_current_player = True
        if self.draw_two_next:
            self.draw_cards(player, 2 * self.draw_two_next)
            self.draw_two_next = 0
            self.skip_current_player = True
        if self.skip_next:
            self.skip_next = False
            self.skip_current_player = True
        if self.skip_current_player:
            self.skip_current_player = False
            self.consecutive_passes = 0
            self.advance_turn()
            return None

        # Liste des cartes jouables (index et cartes)
        playable = [(i, card) for i, card in enumerate(hand) if is_playable(card, top_card, self.current_color)]
        logging.debug(f"[DEBUG] Playable cards for player {player}: {[c for _, c in playable]}")

        if playable:
            if human_input is not None:
                if not isinstance(human_input, int) or human_input < 0 or human_input >= len(hand):
                    raise ValueError("Card index out of bounds.")
                card_str = hand[human_input]
                if (human_input, card_str) not in playable:
                    raise ValueError("Card is not playable.")
                chosen_idx = human_input
                is_human = True
            else:
                if self.agents and self.agents[player]:
                    agent = self.agents[player]
                    idx = agent.choose_action(self.get_state(), player)
                    if idx is None or idx < 0 or idx >= len(hand) or (idx, hand[idx]) not in playable:
                        self.draw_cards(player, 1)
                        self.advance_turn()
                        return None
                    chosen_idx = idx
                    is_human = False
                else:
                    chosen_idx = playable[0][0]
                    is_human = False

            chosen_card = hand[chosen_idx]
            del hand[chosen_idx]
            self.discard_pile.append(chosen_card)

            # Effets spéciaux UNO
            card_lower = chosen_card.lower()
            if "skip" in card_lower:
                self.skip_next = True
            elif "reverse" in card_lower:
                if self.num_players == 2:
                    self.skip_next = True
                else:
                    self.direction *= -1
            elif "+2" in card_lower:
                self.draw_two_next += 1
            elif "+4" in card_lower:
                self.draw_four_next += 1
                if not is_human:
                    colors_in_hand = [card.split()[0] for card in self.hands[player] if card.split()[0] in COLORS]
                    if colors_in_hand:
                        self.current_color = random.choice(colors_in_hand)
                    else:
                        self.current_color = random.choice(COLORS)
            elif "wild" in card_lower:
                if not is_human:
                    # Si IA : choisis une couleur automatiquement
                    colors_in_hand = [card.split()[0] for card in self.hands[player] if card.split()[0] in COLORS]
                    if colors_in_hand:
                        self.current_color = random.choice(colors_in_hand)
                    else:
                        self.current_color = random.choice(COLORS)
                        # Si humain : NE CHANGE PAS current_color ici, attend l'appel à /choose_color
            else:
                self.current_color = chosen_card.split()[0]

        else:
            # Aucune carte jouable : pioche automatiquement
            self.draw_cards(player, 1)
            self.consecutive_passes += 1
        
         # Vérifie la victoire
        if not self.hands[player]:
            return player

        self.advance_turn()
        return None

    def advance_turn(self):
        self.current_player = (self.current_player + self.direction) % self.num_players
        self.turn += 1

    def calculate_scores(self) -> List[int]:
        """
        Calculate the scores for all players.

        Returns:
            List[int]: List of player scores.
        """
        scores = [calculate_score(self.hands, winner_idx=i) for i in range(self.num_players)]
        return scores

    def get_winner(self) -> Optional[int]:
        for i, hand in enumerate(self.hands):
            if len(hand) == 0:
                return i
        return None

    def set_current_color(self, color: str):
        if color in COLORS:
            self.current_color = color
            return True
        return False