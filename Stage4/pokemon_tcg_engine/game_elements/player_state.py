# pokemon_tcg_engine/game_elements/player_state.py
"""Represents the state of a single player in the Pokémon TCG."""

from typing import List, Optional, Set
import random # For shuffling deck

# from ..cards.base_card import BaseCard # Example import
# from ..cards.pokemon_card import PokemonCard # Example import
from .board import PokemonBoard
# from lemon_tcg_lib.lemon_tcg.entities.player import Player as LemonPlayer # If using

class PlayerState:
    """Manages the state and resources of a player."""
    def __init__(self, player_id: str, name: str, deck_list: List[object]):
        self.player_id = player_id
        self.name = name
        self.board = PokemonBoard(player_id=player_id)
        self.initial_deck_list = list(deck_list) # Keep a copy of the original deck for reference
        self.deck: List[object] = []
        self.hand: List[object] = []
        self.discard_pile: List[object] = []
        self.prize_cards: List[object] = []
        self.lost_zone: List[object] = [] # Some cards might go to a lost zone
        self.has_played_supporter_this_turn: bool = False
        self.has_attached_energy_this_turn: bool = False
        self.has_retreated_this_turn: bool = False
        # self.lemon_player_data = LemonPlayer(id=player_id, display_name=name, card_count=len(deck_list), index=0) # Example

    def setup_player(self, num_prize_cards: int = 6, initial_hand_size: int = 7):
        """Initializes the player for a new game: shuffles deck, sets prizes, draws hand."""
        self.deck = list(self.initial_deck_list)
        self.shuffle_deck()
        
        # Set prize cards
        if len(self.deck) < num_prize_cards:
            raise ValueError(f"Player {self.name} does not have enough cards in deck ({len(self.deck)}) to set {num_prize_cards} prize cards.")
        for _ in range(num_prize_cards):
            self.prize_cards.append(self.deck.pop(0))
        
        # Draw initial hand
        self.draw_cards(count=initial_hand_size)
        
        # Reset turn-based flags
        self.reset_turn_flags()
        print(f"Player {self.name} setup complete. Deck: {len(self.deck)}, Hand: {len(self.hand)}, Prizes: {len(self.prize_cards)}")

    def shuffle_deck(self):
        """Shuffles the player's deck."""
        random.shuffle(self.deck)
        print(f"Player {self.name}'s deck shuffled.")

    def draw_cards(self, count: int = 1) -> List[object]:
        """Draws a specified number of cards from the deck to the hand."""
        drawn_cards = []
        for _ in range(count):
            if not self.deck:
                print(f"Player {self.name}'s deck is empty. Cannot draw.")
                # Game logic should handle deck out condition here or at a higher level
                break
            card = self.deck.pop(0)
            self.hand.append(card)
            drawn_cards.append(card)
        print(f"Player {self.name} drew {len(drawn_cards)} card(s). Hand size: {len(self.hand)}.")
        return drawn_cards

    def add_card_to_hand(self, card: object):
        """Adds a specific card to the player's hand (e.g., from search effect)."""
        self.hand.append(card)

    def remove_card_from_hand(self, card: object) -> bool:
        """Removes a specific card from the player's hand. Returns True if successful."""
        try:
            self.hand.remove(card)
            return True
        except ValueError:
            print(f"Card {card.name} not found in player {self.name}'s hand.")
            return False

    def add_card_to_discard(self, card: object):
        """Adds a card to the player's discard pile."""
        self.discard_pile.append(card)
        self.board.add_to_discard(card) # Also update board's view if separate

    def take_prize_card(self) -> Optional[object]:
        """Takes one prize card and adds it to the hand. Returns the card taken or None."""
        if self.prize_cards:
            prize = self.prize_cards.pop(0)
            self.hand.append(prize)
            print(f"Player {self.name} took a prize card: {prize.name}. Prizes remaining: {len(self.prize_cards)}.")
            return prize
        print(f"Player {self.name} has no prize cards left to take.")
        return None

    def reset_turn_flags(self):
        """Resets flags that track turn-limited actions."""
        self.has_played_supporter_this_turn = False
        self.has_attached_energy_this_turn = False
        self.has_retreated_this_turn = False

    def get_all_pokemon_in_play(self) -> List[object]: # PokemonCard type
        """Returns a list of all Pokémon the player has in play (active and benched)."""
        all_pokemon = []
        if self.board.active_pokemon:
            all_pokemon.append(self.board.active_pokemon)
        all_pokemon.extend(self.board.bench)
        return all_pokemon

    def __str__(self) -> str:
        return f"Player: {self.name} (ID: {self.player_id}) - Hand: {len(self.hand)}, Deck: {len(self.deck)}, Discard: {len(self.discard_pile)}, Prizes: {len(self.prize_cards)}"

