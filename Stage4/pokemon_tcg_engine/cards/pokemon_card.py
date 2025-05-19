# pokemon_tcg_engine/cards/pokemon_card.py
"""Represents a Pokémon card with its specific attributes and actions."""

from typing import List, Optional, Dict, Callable, Set
from pydantic import BaseModel, Field, validator

from .base_card import BaseCard #, CardData # If using Pydantic for BaseCard data
from .card_enums import PokemonType, EvolutionStage, StatusCondition

# Placeholder for EnergyCard if we need to represent attached energy units
# Since energy is generated, this might just be a type or a simple class/enum
# For now, we'll use PokemonType to represent energy types for costs and attachments.

class AttackData(BaseModel):
    name: str
    cost: Dict[PokemonType, int] = Field(default_factory=dict)
    damage: int = 0
    effect_description: Optional[str] = None
    # effect_callable: Optional[Callable] # Callable types are hard to serialize directly in Pydantic
                                        # We might store a name/ID and resolve to a function later.

class AbilityData(BaseModel):
    name: str
    description: str
    # effect_callable: Optional[Callable]

class PokemonCardData(BaseModel): # Was CardData, but specific to Pokemon
    card_id: str
    name: str
    description: Optional[str] = None
    hp: int = Field(..., gt=0) # HP must be positive
    pokemon_type: PokemonType
    evolution_stage: EvolutionStage
    evolves_from: Optional[str] = None
    attacks: List[AttackData] = Field(default_factory=list)
    ability: Optional[AbilityData] = None
    weakness_type: Optional[PokemonType] = None
    weakness_multiplier: float = 2.0 # Default, e.g., x2
    resistance_type: Optional[PokemonType] = None
    resistance_value: int = 20 # Default, e.g., -20
    retreat_cost: int = Field(..., ge=0) # Retreat cost can be 0
    is_ex: bool = False

    @validator("evolves_from", always=True)
    def check_evolves_from(cls, v, values):
        if values.get("evolution_stage") != EvolutionStage.BASIC and v is None:
            raise ValueError("evolves_from must be specified for non-Basic Pokémon")
        if values.get("evolution_stage") == EvolutionStage.BASIC and v is not None:
            raise ValueError("evolves_from must not be specified for Basic Pokémon")
        return v

class PokemonCard(BaseCard):
    """Represents a Pokémon card in the game."""
    def __init__(
        self,
        card_id: str,
        name: str,
        hp: int,
        pokemon_type: PokemonType,
        evolution_stage: EvolutionStage,
        attacks: List[AttackData],
        description: Optional[str] = None,
        evolves_from: Optional[str] = None,
        ability: Optional[AbilityData] = None,
        weakness_type: Optional[PokemonType] = None,
        weakness_multiplier: float = 2.0,
        resistance_type: Optional[PokemonType] = None,
        resistance_value: int = 20,
        retreat_cost: int = 0,
        is_ex: bool = False,
        # Runtime attributes
        game_context: Optional[Any] = None # To access game state for effects, etc.
    ):
        super().__init__(card_id, name, description)
        self.hp = hp
        self.current_hp = hp # Initialized when put into play
        self.pokemon_type = pokemon_type
        self.evolution_stage = evolution_stage
        self.evolves_from = evolves_from
        self.attacks = attacks
        self.ability = ability
        self.weakness_type = weakness_type
        self.weakness_multiplier = weakness_multiplier
        self.resistance_type = resistance_type
        self.resistance_value = resistance_value
        self.retreat_cost = retreat_cost
        self.is_ex = is_ex

        # In-game state attributes (managed by PlayerState/Board)
        self.attached_energies: Dict[PokemonType, int] = {ptype: 0 for ptype in PokemonType} # Tracks count of each energy type
        self.status_conditions: Set[StatusCondition] = set()
        self.pokemon_tool_attached: Optional[Any] = None # Should be ToolCard type
        self.damage_counters: int = 0
        self.has_attacked_this_turn: bool = False
        self.is_benched: bool = False
        self.is_active: bool = False
        self.turns_in_play: int = 0 # For evolution rules, etc.

        self.game_context = game_context # For complex effects needing game state access

    def get_card_type(self) -> str:
        return "Pokemon"

    def take_damage(self, amount: int, source_type: Optional[PokemonType] = None) -> int:
        """Applies damage to the Pokémon, considering weakness and resistance."""
        effective_damage = amount
        if source_type:
            if self.weakness_type == source_type:
                effective_damage = int(effective_damage * self.weakness_multiplier)
                print(f"{self.name} is weak to {source_type.name}! Damage multiplied to {effective_damage}.")
            if self.resistance_type == source_type:
                effective_damage = max(0, effective_damage - self.resistance_value)
                print(f"{self.name} resists {source_type.name}! Damage reduced to {effective_damage}.")
        
        self.current_hp -= effective_damage
        self.damage_counters = self.hp - self.current_hp # Assuming damage counters track total damage
        print(f"{self.name} takes {effective_damage} damage. Current HP: {self.current_hp}/{self.hp}")
        
        if self.current_hp <= 0:
            print(f"{self.name} is Knocked Out!")
            # KO logic handled by GameState/ActionResolver
        return effective_damage

    def heal(self, amount: int):
        """Heals damage from the Pokémon."""
        healed_amount = min(amount, self.hp - self.current_hp) # Cannot heal beyond max HP
        self.current_hp += healed_amount
        self.damage_counters = self.hp - self.current_hp
        print(f"{self.name} healed {healed_amount} HP. Current HP: {self.current_hp}/{self.hp}")

    def attach_energy_type(self, energy_type: PokemonType, count: int = 1):
        """Attaches an energy of a specific type (from generated pool)."""
        self.attached_energies[energy_type] = self.attached_energies.get(energy_type, 0) + count
        print(f"{count} {energy_type.name} energy attached to {self.name}. Total: {self.attached_energies}")

    def detach_energy_type(self, energy_type: PokemonType, count: int = 1) -> bool:
        """Detaches energy of a specific type. Returns True if successful."""
        if self.attached_energies.get(energy_type, 0) >= count:
            self.attached_energies[energy_type] -= count
            if self.attached_energies[energy_type] == 0:
                del self.attached_energies[energy_type] # Clean up if zero
            print(f"{count} {energy_type.name} energy detached from {self.name}. Remaining: {self.attached_energies}")
            return True
        print(f"Not enough {energy_type.name} energy on {self.name} to detach {count}.")
        return False

    def can_afford_attack(self, attack_name: str) -> bool:
        """Checks if the Pokémon has enough attached energy to use the specified attack."""
        attack_to_check = next((atk for atk in self.attacks if atk.name == attack_name), None)
        if not attack_to_check:
            return False
        
        # Count total colorless energy provided by all attached energies
        total_colorless_available = sum(self.attached_energies.values())
        # Check specific type costs
        for energy_type, required_count in attack_to_check.cost.items():
            if energy_type == PokemonType.COLORLESS:
                continue # Handled last
            if self.attached_energies.get(energy_type, 0) < required_count:
                return False
            total_colorless_available -= required_count # This energy is now earmarked

        # Check remaining colorless cost
        colorless_cost = attack_to_check.cost.get(PokemonType.COLORLESS, 0)
        return total_colorless_available >= colorless_cost

    def apply_status(self, status: StatusCondition):
        # Some statuses might override others (e.g., Asleep and Paralyzed might not stack)
        # This needs to be defined by game rules.
        self.status_conditions.add(status)
        print(f"{self.name} is now {status.name}.")

    def cure_status(self, status_to_cure: Optional[StatusCondition] = None, cure_all: bool = False):
        if cure_all:
            self.status_conditions.clear()
            print(f"{self.name} is cured of all status conditions.")
        elif status_to_cure and status_to_cure in self.status_conditions:
            self.status_conditions.remove(status_to_cure)
            print(f"{self.name} is no longer {status_to_cure.name}.")

    def can_evolve_from(self, base_pokemon_name: str) -> bool:
        return self.evolution_stage != EvolutionStage.BASIC and self.evolves_from == base_pokemon_name

    def to_dict_ingame(self) -> dict:
        """Returns a dictionary representation of the card including its in-game state."""
        base_info = super().to_dict()
        base_info.update({
            "hp": self.hp,
            "current_hp": self.current_hp,
            "pokemon_type": self.pokemon_type.name,
            "evolution_stage": self.evolution_stage.name,
            "evolves_from": self.evolves_from,
            "attacks": [atk.dict() for atk in self.attacks],
            "ability": self.ability.dict() if self.ability else None,
            "weakness_type": self.weakness_type.name if self.weakness_type else None,
            "weakness_multiplier": self.weakness_multiplier,
            "resistance_type": self.resistance_type.name if self.resistance_type else None,
            "resistance_value": self.resistance_value,
            "retreat_cost": self.retreat_cost,
            "is_ex": self.is_ex,
            "attached_energies": {k.name: v for k, v in self.attached_energies.items()},
            "status_conditions": [s.name for s in self.status_conditions],
            "pokemon_tool_attached": self.pokemon_tool_attached.name if self.pokemon_tool_attached else None,
            "damage_counters": self.damage_counters
        })
        return base_info

    @classmethod
    def from_data(cls, data: PokemonCardData, game_context: Optional[Any] = None) -> "PokemonCard":
        """Creates a PokemonCard instance from a PokemonCardData model."""
        return cls(
            card_id=data.card_id,
            name=data.name,
            description=data.description,
            hp=data.hp,
            pokemon_type=data.pokemon_type,
            evolution_stage=data.evolution_stage,
            evolves_from=data.evolves_from,
            attacks=data.attacks,
            ability=data.ability,
            weakness_type=data.weakness_type,
            weakness_multiplier=data.weakness_multiplier,
            resistance_type=data.resistance_type,
            resistance_value=data.resistance_value,
            retreat_cost=data.retreat_cost,
            is_ex=data.is_ex,
            game_context=game_context
        )

