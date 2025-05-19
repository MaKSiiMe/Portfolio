# pokemon_tcg_engine/cards/base_card.py
"""Base class for all cards in the Pokémon TCG engine."""

from abc import ABC, abstractmethod
from typing import Optional, Any
from pydantic import BaseModel, Field

# Attempt to import from LemonTCG if it's structured as expected
# This is a placeholder for now, actual integration will depend on LemonTCG's structure
# try:
#     from lemon_tcg_lib.lemon_tcg.entities.card import Card as LemonCardBase
# except ImportError:
#     LemonCardBase = object # Fallback if LemonTCG is not available or structured differently

class CardData(BaseModel):
    """Pydantic model for basic card data, can be extended by specific card types."""
    card_id: str = Field(..., description="Unique identifier for the card, e.g., sv1-001")
    name: str = Field(..., description="Name of the card")
    description: Optional[str] = Field(None, description="Flavor text or general description of the card")
    # Add any other common fields that LemonTCG might expect or that are truly universal

class BaseCard(ABC):
    """Abstract base class for all Pokémon TCG cards."""
    def __init__(self, card_id: str, name: str, description: Optional[str] = None):
        self.card_id = card_id
        self.name = name
        self.description = description
        # self.lemon_card_instance = LemonCardBase(...) # If wrapping LemonTCG's card

    @abstractmethod
    def get_card_type(self) -> str:
        """Returns the high-level type of the card (e.g., "Pokemon", "Trainer", "Energy")."""
        pass

    def __str__(self) -> str:
        return f"{self.name} ({self.card_id})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id=\'{self.card_id}\', name=\'{self.name}\')>"

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the card."""
        return {
            "card_id": self.card_id,
            "name": self.name,
            "description": self.description,
            "card_type": self.get_card_type()
        }

    # If using Pydantic models for validation/serialization, you might integrate them here
    # or have factory methods that create BaseCard instances from Pydantic models.
    # @classmethod
    # def from_data(cls, data: CardData) -> "BaseCard":
    #     # This would need to be implemented in subclasses to return the correct card type
    #     raise NotImplementedError

