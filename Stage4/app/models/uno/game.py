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

class Game:
    def __init__(self, num_players: int = 2, seed: Optional[int] = None, agents=None):
        self.num_players = num_players
        self.seed = seed
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
        self.current_color = None  # ✅ NOUVEAU : couleur active séparée
        if agents is not None:
            self.agents = agents
        else:
            # Par défaut, tous les joueurs sont des RuleBasedAgent
            self.agents = [RuleBasedAgent() for _ in range(num_players)]


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
            self.current_color = first_card.split()[0]  # Couleur du premier card


    def handle_first_card(self):
        """
        Handles the first card in the discard pile if it is a special card.
        """
        if self.discard_pile[-1].startswith("Wild"):
            new_color = random.choice(COLORS)
            if "+4" in self.discard_pile[-1]:
                self.discard_pile[-1] = f"{new_color} Wild +4"
                self.draw_four_next = 1
            else:
                self.discard_pile[-1] = f"{new_color} Wild"


    def get_state(self) -> dict:
        """
        Returns the current state of the game.

        Returns:
            dict: Current game state with information about players, deck, discard pile, hands, current player, direction, and turn.
        """
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


    def draw_cards(self, player_idx: int, count: int):
        """
        Draw cards for a player.

        Args:
            player_idx (int): Player index.
            count (int): Number of cards to draw.
        """
        for _ in range(count):
            if not self.deck:
                reshuffle_discard_pile(self.deck, self.discard_pile)
            if self.deck:
                self.hands[player_idx].append(self.deck.pop())


    def play_turn(self, human_input: Optional[int] = None) -> Optional[int]:
        player = self.current_player
        hand = self.hands[player]
        top_card = self.discard_pile[-1]

        if not self.hands[self.current_player]:
            return self.current_player  # Already won


        # Appliquer les effets accumulés
        if self.draw_four_next:
            self.draw_cards(player, 4)
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

        # Cartes jouables
        playable = [card for card in hand if is_playable(card, top_card, self.current_color)]
        
        logging.debug(f"[DEBUG] Playable cards for player {self.current_player}: {playable}")

        if playable:
            if human_input is not None:
                # On suppose que human_input vient d'env.step() et correspond à une carte
                card_str = hand[human_input]
                if card_str not in playable:
                    raise ValueError("Card is not playable.")
                chosen_card = card_str

            else:
                if self.agents and self.agents[player]:
                    agent = self.agents[player]
                    idx = agent.choose_action(self.get_state(), player)

                    if idx is None or idx == len(ALL_CARDS):  # DRAW
                        self.draw_cards(player, 1)
                        self.advance_turn()
                        return None

                    card_str = ALL_CARDS[idx]
                    if card_str not in hand or not is_playable(card_str, top_card, self.current_color):
                        self.draw_cards(player, 1)
                        self.advance_turn()
                        return None

                    chosen_card = card_str
                else:
                    # Aucun agent => tirer une carte
                    self.draw_cards(player, 1)
                    self.advance_turn()
                    return None

            # Appliquer les effets de carte
            self.hands[player].remove(chosen_card)
            self.discard_pile.append(chosen_card)

            if "Skip" in chosen_card:
                self.skip_next = True
            elif "Reverse" in chosen_card:
                self.direction *= -1 if self.num_players > 2 else 1
                if self.num_players == 2:
                    self.skip_next = True
            elif "Wild +4" in chosen_card:
                self.draw_four_next += 1
                self.current_color = self.choose_random_color(self.hands[player])
            elif "Wild" in chosen_card:
                self.current_color = self.choose_random_color(self.hands[player])
            else:
                self.current_color = chosen_card.split()[0]

        else:
            self.draw_cards(player, 1)
            self.consecutive_passes += 1

        # Vérifier victoire
        if len(self.hands[player]) == 0:
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