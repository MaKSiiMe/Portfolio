#!/usr/bin/env python3

from typing import List, Optional
from card import Card, PokemonCard, SupporterCard, ItemCard, ToolCard

class Player:
    def __init__(self, name: str, deck: List[Card]):
        self.name = name
        self.deck: List[Card] = deck
        self.hand: List[Card] = []
        self.discard_pile: List[Card] = []
        self.active_pokemon: Optional[PokemonCard] = None
        self.bench: List[PokemonCard] = []
        self.energy_available: int = 1
        self.energy_used: bool = False
        self.victory_points: int = 0
        self.supporter_played: bool = False
        self.tools_attached: List[ToolCard] = []

    def draw_card(self) -> Optional[Card]:
        if self.deck:
            card = self.deck.pop(0)
            self.hand.append(card)
            return card
        return None

    def draw_starting_hand(self):
        for _ in range(5):
            self.draw_card()

    def play_pokemon_to_bench(self, pokemon: PokemonCard) -> bool:
        if isinstance(pokemon, PokemonCard) and pokemon in self.hand and len(self.bench) < 3:
            self.hand.remove(pokemon)
            self.bench.append(pokemon)
            return True
        return False

    def set_active_pokemon(self, pokemon: PokemonCard) -> bool:
        if isinstance(pokemon, PokemonCard) and pokemon in self.hand:
            self.hand.remove(pokemon)
            self.active_pokemon = pokemon
            return True
        return False

    def attach_energy(self, pokemon: PokemonCard) -> bool:
        if self.energy_available > 0 and not self.energy_used:
            pokemon.energy_attached += 1
            self.energy_used = True
            return True
        return False

    def play_supporter(self, supporter: SupporterCard) -> bool:
        if isinstance(supporter, SupporterCard) and supporter in self.hand and not self.supporter_played:
            self.hand.remove(supporter)
            self.discard_pile.append(supporter)
            self.supporter_played = True
            return True
        return False

    def play_item(self, item: ItemCard) -> bool:
        if isinstance(item, ItemCard) and item in self.hand:
            self.hand.remove(item)
            self.discard_pile.append(item)
            return True
        return False

    def attach_tool(self, tool: ToolCard, target: PokemonCard) -> bool:
        if isinstance(tool, ToolCard) and tool in self.hand and tool.attached_to is None:
            tool.attached_to = target
            self.tools_attached.append(tool)
            self.hand.remove(tool)
            return True
        return False

    def evolve_pokemon(self, base_pokemon: PokemonCard, evolved_form: PokemonCard) -> bool:
        if evolved_form.evolution != "Stage 1" and evolved_form.evolution != "Stage 2":
            return False
        if evolved_form in self.hand:
            for i, p in enumerate(self.bench):
                if p.name == base_pokemon.name:
                    self.bench[i] = evolved_form
                    self.hand.remove(evolved_form)
                    return True
            if self.active_pokemon and self.active_pokemon.name == base_pokemon.name:
                self.active_pokemon = evolved_form
                self.hand.remove(evolved_form)
                return True
        return False

    def gain_point(self, pokemon: PokemonCard):
        points = 2 if pokemon.is_ex else 1
        self.victory_points += points

    def has_won(self) -> bool:
        return self.victory_points >= 3

    def reset_turn_flags(self):
        self.energy_used = False
        self.supporter_played = False
        for tool in self.tools_attached:
            tool.used_this_turn = False
        if self.active_pokemon and self.active_pokemon.talent:
            self.active_pokemon.talent.used_this_turn = False

    def take_damage(self, damage: int):
        if self.active_pokemon:
            self.active_pokemon.current_hp = max(0, self.active_pokemon.current_hp - damage)
            print(f"{self.active_pokemon.name} subit {damage} dégâts. HP restants : {self.active_pokemon.current_hp}")
            if self.active_pokemon.is_knocked_out():
                print(f"{self.active_pokemon.name} est mis K.O. !")
                self.discard_pile.append(self.active_pokemon)
                self.active_pokemon = None
