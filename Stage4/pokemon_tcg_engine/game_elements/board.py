# pokemon_tcg_engine/game_elements/board.py
"""Represents the game board and its various zones for Pokémon TCG Pocket."""

from typing import List, Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..cards.base_card import BaseCard
    from ..cards.pokemon_card import PokemonCard
    from ..cards.trainer_card import StadiumCard # If Stadiums are used

MAX_BENCH_SIZE_POCKET = 3 # As per rules.md for Pokémon TCG Pocket

class PokemonBoard:
    """Manages the different zones on a player's side of the Pokémon TCG Pocket board."""
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.active_pokemon_slot: Optional["PokemonCard"] = None
        # Bench is a list of fixed size, containing PokemonCard or None
        self.bench: List[Optional["PokemonCard"]] = [None] * MAX_BENCH_SIZE_POCKET
        self.discard_pile: List["BaseCard"] = []
        self.lost_zone: List["BaseCard"] = []
        # Note: Deck, Hand, Prize Cards, and Available Energies are primarily managed by PlayerState

    def place_on_active(self, pokemon_card: "PokemonCard") -> bool:
        """Places a Pokémon in the active slot. Assumes previous active is handled (KO, retreat)."""
        if self.active_pokemon_slot is None:
            self.active_pokemon_slot = pokemon_card
            pokemon_card.is_active = True
            pokemon_card.is_benched = False
            print(f"{pokemon_card.name} moved to active slot for player {self.player_id}.")
            return True
        else:
            print(f"Error: Active slot for player {self.player_id} is already occupied by {self.active_pokemon_slot.name}. Handle KO or retreat first.")
            return False

    def add_to_bench(self, pokemon_card: "PokemonCard") -> bool:
        """Adds a Pokémon to an empty spot on the bench. Returns True if successful."""
        for i, spot in enumerate(self.bench):
            if spot is None:
                self.bench[i] = pokemon_card
                pokemon_card.is_benched = True
                pokemon_card.is_active = False
                print(f"{pokemon_card.name} added to bench spot {i} for player {self.player_id}.")
                return True
        print(f"Bench for player {self.player_id} is full. Cannot add {pokemon_card.name}.")
        return False

    def remove_from_active(self) -> Optional["PokemonCard"]:
        """Removes and returns the Pokémon from the active slot. Used for KO, retreat, etc."""
        pokemon = self.active_pokemon_slot
        if pokemon:
            pokemon.is_active = False
            self.active_pokemon_slot = None
            print(f"{pokemon.name} removed from active slot for player {self.player_id}.")
        return pokemon

    def remove_from_bench(self, pokemon_to_remove: "PokemonCard") -> bool:
        """Removes a specific Pokémon from the bench. Returns True if successful."""
        try:
            index = self.bench.index(pokemon_to_remove)
            self.bench[index].is_benched = False
            self.bench[index] = None
            print(f"{pokemon_to_remove.name} removed from bench for player {self.player_id}.")
            return True
        except ValueError:
            print(f"Error: {pokemon_to_remove.name} not found on the bench for player {self.player_id}.")
            return False
        
    def get_bench_pokemon_at_index(self, index: int) -> Optional["PokemonCard"]:
        if 0 <= index < MAX_BENCH_SIZE_POCKET:
            return self.bench[index]
        return None

    def get_active_pokemon(self) -> Optional["PokemonCard"]:
        return self.active_pokemon_slot

    def get_bench_pokemon(self) -> List["PokemonCard"]:
        """Returns a list of Pokémon currently on the bench (filters out None spots)."""
        return [p for p in self.bench if p is not None]

    def get_all_pokemon_in_play(self) -> List["PokemonCard"]:
        """Returns a list of all Pokémon the player has in play (active and benched)."""
        all_pokemon: List["PokemonCard"] = []
        if self.active_pokemon_slot:
            all_pokemon.append(self.active_pokemon_slot)
        all_pokemon.extend(self.get_bench_pokemon())
        return all_pokemon

    def add_to_discard(self, card: "BaseCard"):
        self.discard_pile.append(card)
        # print(f"Card {card.name} added to discard pile for player {self.player_id}.")

    def add_to_lost_zone(self, card: "BaseCard"):
        self.lost_zone.append(card)
        print(f"Card {card.name} added to lost zone for player {self.player_id}.")

    def is_bench_full(self) -> bool:
        return all(spot is not None for spot in self.bench)

    def promote_from_bench_to_active(self, bench_pokemon: "PokemonCard") -> bool:
        """Promotes a Pokémon from the bench to the active slot. Assumes active is empty."""
        if self.active_pokemon_slot is not None:
            print(f"Error: Cannot promote {bench_pokemon.name}, active slot is occupied by {self.active_pokemon_slot.name}.")
            return False
        
        if bench_pokemon not in self.bench:
            print(f"Error: {bench_pokemon.name} is not on the bench of player {self.player_id}.")
            return False

        # Remove from bench
        bench_index = -1
        for i, p_card in enumerate(self.bench):
            if p_card == bench_pokemon:
                bench_index = i
                break
        
        if bench_index != -1:
            self.bench[bench_index] = None # Vacate bench spot
            bench_pokemon.is_benched = False
            # Place on active
            self.active_pokemon_slot = bench_pokemon
            bench_pokemon.is_active = True
            print(f"{bench_pokemon.name} promoted from bench to active for player {self.player_id}.")
            return True
        return False # Should not happen if bench_pokemon was in self.bench

    def __str__(self) -> str:
        active_name = self.active_pokemon_slot.name if self.active_pokemon_slot else "None"
        bench_names = [p.name if p else "Empty" for p in self.bench]
        return f"Player {self.player_id} Board: Active={active_name}, Bench={bench_names}, Discard={len(self.discard_pile)}"

class GlobalBoardState:
    """Manages elements shared by both players, like the active Stadium card.
       For Pokémon TCG Pocket, rules.md does not explicitly mention Stadiums.
       This class is included for completeness but might be simplified or removed if Stadiums are not in Pocket.
    """
    def __init__(self):
        self.active_stadium: Optional["StadiumCard"] = None

    def set_active_stadium(self, stadium_card: "StadiumCard", previous_stadium_owner_board: Optional[PokemonBoard] = None):
        """Sets the active stadium, discarding the previous one if any."""
        if self.active_stadium and previous_stadium_owner_board:
            # The game logic should handle adding the old stadium to the correct discard pile.
            print(f"Stadium {self.active_stadium.name} is replaced and should be discarded.")
            # previous_stadium_owner_board.add_to_discard(self.active_stadium) # Game logic should do this.
        
        self.active_stadium = stadium_card
        if stadium_card:
            print(f"Stadium {stadium_card.name} is now active.")
            # stadium_card.on_play() # Stadium applies its effect
        else:
            # if self.active_stadium: # If an old stadium was just removed
            #    self.active_stadium.on_discard() # Stadium removes its effect
            print("No stadium is active.")

    def get_active_stadium(self) -> Optional["StadiumCard"]:
        return self.active_stadium

    def discard_active_stadium(self, owner_board: Optional[PokemonBoard] = None):
        if self.active_stadium:
            print(f"Stadium {self.active_stadium.name} is discarded.")
            # self.active_stadium.on_discard()
            # Game logic should add it to the owner's discard pile if applicable.
            # if owner_board: owner_board.add_to_discard(self.active_stadium)
            self.active_stadium = None

