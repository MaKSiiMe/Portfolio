import random
import time
from typing import List, Optional

from app.models.uno.constants import (
    COLORS, VALUES, SPECIAL_CARDS, WILD_CARDS, CARDS_PER_PLAYER
)
from app.models.uno.deck import create_deck, reshuffle_discard_pile
from app.models.uno.rules import is_playable, calculate_score

class Game:
    """
    Main class to manage the UNO card game.
    """

    def __init__(self, num_players: int = 2, seed: Optional[int] = None):
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

    def start(self):
        for i in range(self.num_players):
            self.hands[i] = [self.deck.pop() for _ in range(CARDS_PER_PLAYER)]
        self.discard_pile.append(self.deck.pop())
        self.handle_first_card()

    def handle_first_card(self):
        if self.discard_pile[-1].startswith("Wild"):
            new_color = random.choice(COLORS)
            if "+4" in self.discard_pile[-1]:
                self.discard_pile[-1] = f"{new_color} Wild +4"
                self.draw_four_next = 1
            else:
                self.discard_pile[-1] = f"{new_color} Wild"

    def get_state(self) -> dict:
        winner = None
        for idx, hand in enumerate(self.hands):
            if len(hand) == 0:
                winner = idx
                break
    
        print(f"[get_state] Joueur actuel : {self.current_player}")
        print(f"[get_state] Mains : {[len(h) for h in self.hands]}")
        print(f"[get_state] Gagnant : {winner}")
    
        return {
            "num_players": self.num_players,
            "deck_size": len(self.deck),
            "discard_pile": [parse_card(card) for card in self.discard_pile],
            "hands": [[parse_card(card) for card in hand] for hand in self.hands],
            "current_player": self.current_player,
            "direction": self.direction,
            "turn": self.turn,
            "winner": winner
    }

    def draw_cards(self, player_idx: int, count: int):
        for _ in range(count):
            if not self.deck:
                reshuffle_discard_pile(self.deck, self.discard_pile)
            if self.deck:
                self.hands[player_idx].append(self.deck.pop())

    def play_turn(self, human_input: Optional[int] = None) -> Optional[int]:
        hand = self.hands[self.current_player]
        top_card = self.discard_pile[-1]

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

        playable = [card for card in hand if is_playable(card, top_card)]

        if playable:
            if human_input is not None:
                if 0 <= human_input < len(playable):
                    chosen_card = playable[human_input]
                else:
                    raise ValueError("Invalid choice.")
            else:
                chosen_card = playable[0]

            hand.remove(chosen_card)
            self.discard_pile.append(chosen_card)
            self.consecutive_passes = 0

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
            return self.current_player

        self.advance_turn()
        return None

    def advance_turn(self):
        self.current_player = (self.current_player + self.direction) % self.num_players
        self.turn += 1

    def calculate_scores(self) -> List[int]:
        return [calculate_score(self.hands, winner_idx=i) for i in range(self.num_players)]

    def serialize(self):
        return self.get_state()

    def play_bot_turn(self):
        """
        Fait automatiquement jouer le bot (joueur 1) tant que ce n'est pas le tour du joueur humain (0).
        """
        bot_idx = self.current_player

        print(f"[Bot] C'est au tour du bot (joueur {bot_idx})")
        bot_hand = self.hands[bot_idx]
        top_card = self.discard_pile[-1]
        print(f"[Bot] Carte au sommet : {top_card}")
        print(f"[Bot] Main du bot avant : {bot_hand}")

        playable = [card for card in bot_hand if is_playable(card, top_card)]

        if not playable:
            print("[Bot] Aucune carte jouable. Il pioche.")
            self.draw_cards(bot_idx, 1)
            playable = [card for card in self.hands[bot_idx] if is_playable(card, top_card)]
        if not playable:
            print("[Bot] Toujours aucune carte jouable après pioche. Fin du tour.")
            self.advance_turn()
            return

        chosen = playable[0]
        self.hands[bot_idx].remove(chosen)

        # Choix de couleur pour Joker
        if "Wild" in chosen:
            colors = ['red', 'green', 'blue', 'yellow']
            chosen_color = random.choice(colors)
            value = chosen.split(' ', 1)[1]
            chosen = f"{chosen_color} {value}"
            print(f"[Bot] Joue une carte Wild. Nouvelle couleur : {chosen_color}")

            if "+4" in chosen:
                self.draw_four_next += 1

        self.discard_pile.append(chosen)
        print(f"[Bot] Joue : {chosen}")

        # Effets
        if "+2" in chosen:
            self.draw_two_next += 1
        elif "Skip" in chosen:
            self.skip_next = True
        elif "Reverse" in chosen:
            if self.num_players == 2:
                self.skip_next = True
            else:
                self.direction *= -1

        print(f"[Bot] Main du bot après : {self.hands[bot_idx]}")
        print("---")

        self.advance_turn()
    

def parse_card(card):
    if isinstance(card, dict):
        return card
    elif isinstance(card, str):
        parts = card.split(" ", 1)
        return {"color": parts[0], "value": parts[1]}
    else:
        raise ValueError("Card format not recognized")