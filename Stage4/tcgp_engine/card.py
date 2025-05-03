#!/usr/bin/env python3

class Card:
    def __init__(self, name, card_type):
        self.name = name
        self.card_type = card_type # e.g. "Pokemon", "Supporter", "Item"

        
class PokemonCard(Card):
    def __init__(self, name, hp, stage, attacks, is_ex=False, weakness=None):
        super().__init__(name, "Pokemon")
        self.hp = hp
        self.current_hp = hp
        self.stage = stage  # "Base", "Stage 1", "Stage 2"
        self.attacks = attacks  # List of Attack objects or dicts
        self.is_ex = is_ex
        self.weakness = weakness
        self.energy_attached = 0
        self.status = None  # "Burned", "Poisoned", etc.

    def is_knocked_out(self):
        return self.current_hp <= 0
