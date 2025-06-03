import random
import time
from collections import deque

random.seed(time.time())

COLORS = ["Red", "Green", "Blue", "Yellow"]
VALUES = list(map(str, range(0, 10)))  # "0" to "9"

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def matches(self, other_card):
        return self.color == other_card.color or self.value == other_card.value

    def __repr__(self):
        return f"{self.color} {self.value}"

class Deck:
    def __init__(self):
        self.cards = self._create_deck()
        random.shuffle(self.cards)

    def _create_deck(self):
        cards = []
        for color in COLORS:
            for value in VALUES:
                cards.append(Card(color, value))
                if value != "0":
                    cards.append(Card(color, value))  # Deux de chaque sauf les 0
        return cards

    def draw_card(self):
        if not self.cards:
            raise ValueError("Deck is empty!")
        return self.cards.pop()

    def is_empty(self):
        return len(self.cards) == 0

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck, num=1):
        for _ in range(num):
            if not deck.is_empty():
                self.hand.append(deck.draw_card())

    def get_valid_moves(self, top_card):
        return [card for card in self.hand if card.matches(top_card)]

    def play_turn(self, top_card):
        valid_moves = self.get_valid_moves(top_card)
        if valid_moves:
            chosen = random.choice(valid_moves)
            self.hand.remove(chosen)
            return chosen
        return None

    def has_won(self):
        return len(self.hand) == 0

    def __repr__(self):
        return f"{self.name}: {[str(card) for card in self.hand]}"

class UnoGame:
    def __init__(self, num_players=2, seed=None):
        if seed is not None:
            random.seed(seed)
        self.deck = Deck()
        self.players = [Player(f"Player {i}") for i in range(num_players)]
        self.discard_pile = deque()
        self.current_player_idx = 0
        self.direction = 1  # +1 = clockwise
        self._deal_cards()
        self.discard_pile.append(self.deck.draw_card())

    def _deal_cards(self, cards_per_player=7):
        for player in self.players:
            player.draw(self.deck, cards_per_player)

    def current_player(self):
        return self.players[self.current_player_idx]

    def next_player_index(self):
        return (self.current_player_idx + self.direction) % len(self.players)

    def play(self, verbose=False, max_turns=1000):
        turn = 0
        while turn < max_turns:
            player = self.current_player()
            top_card = self.discard_pile[-1]

            if verbose:
                print(f"\nTurn {turn} - {player.name}'s turn")
                print(f"Top card: {top_card}")
                print(player)

            played_card = player.play_turn(top_card)

            if played_card:
                self.discard_pile.append(played_card)
                if verbose:
                    print(f"{player.name} plays {played_card}")
            else:
                player.draw(self.deck)
                if verbose:
                    print(f"{player.name} draws a card")

            if player.has_won():
                if verbose:
                    print(f"\n{player.name} wins!")
                return player.name

            self.current_player_idx = self.next_player_index()
            turn += 1

        if verbose:
            print("Max turns reached. Game ended in a draw.")
        return None

if __name__ == "__main__":
    game = UnoGame(num_players=2, seed=42)
    winner = game.play(verbose=True)
