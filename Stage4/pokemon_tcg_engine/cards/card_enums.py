# pokemon_tcg_engine/cards/card_enums.py
"""Enumerations for card properties."""

from enum import Enum, auto

class PokemonType(Enum):
    GRASS = auto()
    FIRE = auto()
    WATER = auto()
    LIGHTNING = auto()
    PSYCHIC = auto()
    FIGHTING = auto()
    DARKNESS = auto()
    METAL = auto()
    DRAGON = auto()
    COLORLESS = auto()


class EvolutionStage(Enum):
    BASIC = auto()
    STAGE_1 = auto()
    STAGE_2 = auto()
    # Add V, VMAX, VSTAR etc. if they are in Pokémon TCG Pocket and detailed in rules
    # For now, keeping it to Base, Stage 1, Stage 2 as per rules.md

class TrainerType(Enum):
    ITEM = auto()
    SUPPORTER = auto()
    TOOL = auto()
    FOSSIL = auto()

class StatusCondition(Enum):
    POISONED = auto()
    BURNED = auto()
    ASLEEP = auto()
    PARALYZED = auto()
    CONFUSED = auto()

