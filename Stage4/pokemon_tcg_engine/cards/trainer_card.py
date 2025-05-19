# pokemon_tcg_engine/cards/trainer_card.py
"""Represents Trainer cards with their specific types and effects."""

from typing import Optional, Any, List
from pydantic import BaseModel, Field

from .base_card import BaseCard #, CardData
from .card_enums import TrainerType, PokemonType # PokemonType for Fossil-as-Pokemon
# from .pokemon_card import PokemonCardData # For Fossil cards that become Pokémon

class TrainerCardData(BaseModel): # Was CardData, specific to Trainer
    card_id: str
    name: str
    description: Optional[str] = None
    trainer_type: TrainerType
    # For Fossil cards that turn into Pokémon upon play
    becomes_pokemon_data: Optional[Any] = None # Placeholder for PokemonCardData if it's a Fossil

class TrainerCard(BaseCard):
    """Base class for all Trainer cards."""
    def __init__(
        self,
        card_id: str,
        name: str,
        trainer_type: TrainerType,
        description: Optional[str] = None,
        game_context: Optional[Any] = None # To access game state for effects
    ):
        super().__init__(card_id, name, description)
        self.trainer_type = trainer_type
        self.game_context = game_context

    def get_card_type(self) -> str:
        return "Trainer"

    def play_effect(self, player, targets: Optional[List[Any]] = None):
        """Applies the effect of the Trainer card.
        This method should be implemented by subclasses or handled by the EffectEngine.
        `player` is the PlayerState of the player playing the card.
        `targets` is an optional list of target cards or players for the effect.
        """
        print(f"{player.name} plays {self.name} ({self.trainer_type.name}). Effect needs to be implemented.")
        # Specific logic will be in subclasses or delegated to an EffectEngine
        # based on self.card_id or self.name for unique effects.
        pass

    def to_dict_ingame(self) -> dict:
        base_info = super().to_dict()
        base_info.update({
            "trainer_type": self.trainer_type.name
        })
        return base_info

    @classmethod
    def from_data(cls, data: TrainerCardData, game_context: Optional[Any] = None) -> "TrainerCard":
        """Creates a TrainerCard instance from TrainerCardData."""
        if data.trainer_type == TrainerType.ITEM:
            return ItemCard.from_data(data, game_context)
        elif data.trainer_type == TrainerType.SUPPORTER:
            return SupporterCard.from_data(data, game_context)
        elif data.trainer_type == TrainerType.TOOL:
            return ToolCard.from_data(data, game_context)
        elif data.trainer_type == TrainerType.STADIUM:
            return StadiumCard.from_data(data, game_context)
        elif data.trainer_type == TrainerType.FOSSIL:
            return FossilCard.from_data(data, game_context)
        # Fallback or raise error
        return cls(data.card_id, data.name, data.trainer_type, data.description, game_context)

class ItemCard(TrainerCard):
    """Represents an Item card. Can be played multiple times per turn."""
    def __init__(self, card_id: str, name: str, description: Optional[str] = None, game_context: Optional[Any] = None):
        super().__init__(card_id, name, TrainerType.ITEM, description, game_context)

    @classmethod
    def from_data(cls, data: TrainerCardData, game_context: Optional[Any] = None) -> "ItemCard":
        return cls(data.card_id, data.name, data.description, game_context)

class SupporterCard(TrainerCard):
    """Represents a Supporter card. Only one can be played per turn."""
    def __init__(self, card_id: str, name: str, description: Optional[str] = None, game_context: Optional[Any] = None):
        super().__init__(card_id, name, TrainerType.SUPPORTER, description, game_context)

    @classmethod
    def from_data(cls, data: TrainerCardData, game_context: Optional[Any] = None) -> "SupporterCard":
        return cls(data.card_id, data.name, data.description, game_context)

class ToolCard(TrainerCard):
    """Represents a Pokémon Tool card. Attaches to a Pokémon."""
    def __init__(self, card_id: str, name: str, description: Optional[str] = None, game_context: Optional[Any] = None):
        super().__init__(card_id, name, TrainerType.TOOL, description, game_context)

    def on_attach(self, pokemon):
        print(f"{self.name} attached to {pokemon.name}. Ongoing effect needs implementation.")
        # Apply immediate or ongoing effects to the Pokémon
        pass

    def on_detach(self, pokemon):
        print(f"{self.name} detached from {pokemon.name}.")
        # Remove ongoing effects if any
        pass

    @classmethod
    def from_data(cls, data: TrainerCardData, game_context: Optional[Any] = None) -> "ToolCard":
        return cls(data.card_id, data.name, data.description, game_context)

class StadiumCard(TrainerCard):
    """Represents a Stadium card. Affects both players and remains in play."""
    def __init__(self, card_id: str, name: str, description: Optional[str] = None, game_context: Optional[Any] = None):
        super().__init__(card_id, name, TrainerType.STADIUM, description, game_context)

    def on_play(self):
        print(f"Stadium {self.name} is now in play. Global effect needs implementation.")
        # Apply global effect
        pass

    def on_discard(self):
        print(f"Stadium {self.name} is discarded.")
        # Remove global effect
        pass

    @classmethod
    def from_data(cls, data: TrainerCardData, game_context: Optional[Any] = None) -> "StadiumCard":
        return cls(data.card_id, data.name, data.description, game_context)

class FossilCard(TrainerCard):
    """Represents a Fossil card. Played as a Trainer, becomes a Basic Pokémon on the Bench."""
    # This card is special. When played, it results in a Pokémon being put onto the Bench.
    # The FossilCard itself might be discarded, and a specific PokemonCard instance created.
    # Or, this card could transform its type in-game (more complex).
    def __init__(self, card_id: str, name: str, description: Optional[str] = None, 
                 becomes_pokemon_data: Optional[Any] = None, # PokemonCardData for the Pokémon it becomes
                 game_context: Optional[Any] = None):
        super().__init__(card_id, name, TrainerType.FOSSIL, description, game_context)
        self.becomes_pokemon_data = becomes_pokemon_data # This should be PokemonCardData

    def play_effect(self, player, targets: Optional[List[Any]] = None):
        # from .pokemon_card import PokemonCard # Local import to avoid circular dependency at module level
        print(f"{player.name} plays Fossil card {self.name}. It will become a Pokémon.")
        if self.becomes_pokemon_data:
            # pokemon_to_bench = PokemonCard.from_data(self.becomes_pokemon_data, self.game_context)
            # player.board.add_to_bench(pokemon_to_bench)
            # print(f"{pokemon_to_bench.name} (from {self.name}) placed on {player.name}"s Bench.")
            # This Fossil card would then typically go to the discard pile.
            # player.discard_pile.append(self)
            print(f"Fossil {self.name} effect: create and bench Pokémon {self.becomes_pokemon_data.name if self.becomes_pokemon_data else 'Unknown'}")
        else:
            print(f"Error: Fossil card {self.name} is missing data for the Pokémon it becomes.")

    @classmethod
    def from_data(cls, data: TrainerCardData, game_context: Optional[Any] = None) -> "FossilCard":
        return cls(data.card_id, data.name, data.description, data.becomes_pokemon_data, game_context)

