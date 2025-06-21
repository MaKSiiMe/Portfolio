from typing import List, Optional
import random
import time

from app.models.uno.constants import COLORS, VALUES, SPECIAL_CARDS, WILD_CARDS, CARDS_PER_PLAYER
from app.models.uno.deck import create_deck, reshuffle_discard_pile
from app.models.uno.rules import is_playable, calculate_score


class Game:
    def __init__(self, num_players: int = 2, seed: Optional[int] = None):
        self.num_players = num_players
        self.seed = seed
        self.deck = create_deck(seed)
        self.hands: List[List[str]] = [[] for _ in range(num_players)]
        self.discard_pile: List[str] = []
        self.current_player = 0
        self.direction = 1  # 1 = sens horaire, -1 = antihoraire
        self.draw_two_next = 0
        self.draw_four_next = 0
        self.skip_next = False
        self.skip_current_player = False
        self.consecutive_passes = 0
        self.turn = 0

    def start(self):
        """Initialise le jeu : distribution des cartes et première carte sur la défausse."""
        for i in range(self.num_players):
            self.hands[i] = [self.deck.pop() for _ in range(CARDS_PER_PLAYER)]

        # Première carte défaussée
        self.discard_pile.append(self.deck.pop())
        self.handle_first_card()

    def handle_first_card(self):
        """Gère les cas spéciaux si la première carte est un Joker ou un +4."""
        if self.discard_pile[-1].startswith("Wild"):
            new_color = random.choice(COLORS)
            if "+4" in self.discard_pile[-1]:
                self.discard_pile[-1] = f"{new_color} Wild +4"
                self.draw_four_next = 1
            else:
                self.discard_pile[-1] = f"{new_color} Wild"

    def get_state(self) -> dict:
        """Retourne l’état courant de la partie (utile pour l’API)."""
        return {
            "num_players": self.num_players,
            "deck_size": len(self.deck),
            "discard_pile": self.discard_pile,
            "hands": self.hands,
            "current_player": self.current_player,
            "direction": self.direction,
            "turn": self.turn
        }

    def draw_cards(self, player_idx: int, count: int):
        for _ in range(count):
            if not self.deck:
                reshuffle_discard_pile(self.deck, self.discard_pile)
            if self.deck:
                self.hands[player_idx].append(self.deck.pop())

    def play_turn(self, human_input: Optional[int] = None) -> Optional[int]:
        """
        Joue un tour complet.
        Si `human_input` est fourni, il s'agit de l'indice de la carte choisie par le joueur humain.
        Retourne l'indice du joueur gagnant si victoire, sinon None.
        """
        hand = self.hands[self.current_player]
        top_card = self.discard_pile[-1]

        # Gérer effets en attente
        if self.draw_four_next:
            self.draw_cards(self.current_player, 4)
            self.draw_four_next = 0
            self.skip_current_player = True

        if self.draw_two_next:
            self.draw_cards(self.current_player, 2 * self.draw_two_next)
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
        playable = [card for card in hand if is_playable(card, top_card)]

        if playable:
            if human_input is not None:
                if 0 <= human_input < len(playable):
                    chosen_card = playable[human_input]
                else:
                    raise ValueError("Choix invalide.")
            else:
                chosen_card = playable[0]  # Simple IA : joue la première carte valide

            hand.remove(chosen_card)
            self.discard_pile.append(chosen_card)
            self.consecutive_passes = 0

            # Effets spéciaux
            if "+2" in chosen_card:
                self.draw_two_next += 1
            elif "Skip" in chosen_card:
                self.skip_next = True
            elif "Reverse" in chosen_card:
                if self.num_players == 2:
                    self.skip_next = True
                else:
                    self.direction *= -1
            elif "Wild +4" in chosen_card:
                new_color = random.choice(COLORS)
                self.discard_pile[-1] = f"{new_color} Wild +4"
                self.draw_four_next += 1
            elif "Wild" in chosen_card:
                new_color = random.choice(COLORS)
                self.discard_pile[-1] = f"{new_color} Wild"

        else:
            self.draw_cards(self.current_player, 1)
            self.consecutive_passes += 1

        if len(hand) == 0:
            return self.current_player  # Victoire

        if self.consecutive_passes >= self.num_players:
            return -1  # Match nul

        self.advance_turn()
        return None

    def advance_turn(self):
        self.current_player = (self.current_player + self.direction) % self.num_players
        self.turn += 1

    def calculate_scores(self) -> List[int]:
        scores = [calculate_score(self.hands, winner=i) for i in range(self.num_players)]
        return scores
