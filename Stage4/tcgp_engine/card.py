#!/usr/bin/env python3
"""
card.py

This module defines the core card classes used in the Pokémon TCG Pocket engine.

Author: Maxime
Date: 2025-05-03
"""

from typing import List, Optional, Dict, Union

class Card:
    def __init__(self, name: str, card_type: str, description: Optional[str] = None):
        """
        Base class for all cards.

        Args:
            name (str): The name of the card.
            card_type (str): The type of the card ("Pokemon", "Supporter", "Item", "Tool").
            description (str, optional): An optional description of the card.
        """
        self.name = name
        self.card_type = card_type
        self.description = description

class PokemonCard(Card):
    def __init__(
        self,
        name: str,
        hp: int,
        evolution: str,
        attacks: List['Attack'],
        pokemon_type: str,
        talent: Optional['Talent'] = None,
        is_ex: bool = False,
        weakness: Optional[Dict[str, Union[str, int]]] = None,
        retreat_cost: int = 0,
        description: Optional[str] = None
    ):
        """
        Represents a Pokémon card in the game.

        Args:
            name (str): The name of the Pokémon card.
            hp (int): The maximum hit points of the Pokémon.
            evolution (str): The evolution stage ("Base", "Stage 1", "Stage 2").
            attacks (List[Attack]): A list of attack objects.
            pokemon_type (str): The type of the Pokémon ("Fire", "Water", etc.).
            talent (Talent, optional): A special ability if the Pokémon has one.
            is_ex (bool): True if the Pokémon is an EX card, False otherwise.
            weakness (dict, optional): A dictionary defining the Pokémon's weakness (e.g. {"type": "Fire", "modifier": 20}).
            retreat_cost (int): The energy cost to retreat this Pokémon.
            description (str, optional): An optional description of the Pokémon card.
        """
        super().__init__(name, card_type="Pokemon", description=description)
        self.hp = hp
        self.current_hp = hp
        self.evolution = evolution
        self.attacks = attacks
        self.talent = talent
        self.pokemon_type = pokemon_type
        self.is_ex = is_ex
        self.weakness = weakness
        self.retreat_cost = retreat_cost
        self.energy_attached = 0
        self.status = None

    def is_knocked_out(self) -> bool:
        """
        Checks whether the Pokémon is knocked out (HP reduced to 0 or less).

        Returns:
            bool: True if the Pokémon is knocked out, False otherwise.
        """
        return self.current_hp <= 0

class SupporterCard(Card):
    def __init__(self, name: str, effect: str, description: Optional[str] = None):
        """
        Represents a Supporter card with a one-time powerful effect.

        Args:
            name (str): The name of the Supporter card.
            effect (str): The effect text or logic of the card.
            description (str, optional): Optional description of the card.
        """
        super().__init__(name, "Supporter", description)
        self.effect = effect

class ItemCard(Card):
    def __init__(self, name: str, effect: str,description: Optional[str] = None):
        """
        Represents an Item card with a utility effect.

        Args:
            name (str): The name of the Item card.
            effect (str): The effect text or logic of the card.
            description (str, optional): Optional description of the card.
        """
        super().__init__(name, "Item", description)
        self.effect = effect

class ToolCard(Card):
    def __init__(self, name: str, effect: str, description: Optional[str] = None):
        """
        Represents a Tool card that can be attached to a Pokémon for passive bonuses.

        Args:
            name (str): The name of the Tool card.
            effect (str): The effect granted by the tool.
            description (str, optional): Optional description of the card.
        """
        super().__init__(name, "Tool", description)
        self.effect = effect
        self.attached_to = None

class Attack:
    def __init__(self, name: str, cost: List[str], damage: int, effect: Optional[str] = None):
        """
        Represents an attack that a Pokémon can use.

        Args:
            name (str): The name of the attack.
            cost (List[str]): List of energy types required (e.g., ["Plant", "Colorless"]).
            damage (int): The amount of damage this attack deals.
            effect (str, optional): Additional effect of the attack.
        """
        self.name = name
        self.cost = cost
        self.damage = damage
        self.effect = effect

class Talent:
    def __init__(self, name: str, effect: str):
        """
        Represents a Talent — a passive or activated ability of a Pokémon.

        Args:
            name (str): The name of the talent.
            effect (str): Description of what the talent does.
        """
        self.name = name
        self.effect = effect
        self.used_this_turn = False
