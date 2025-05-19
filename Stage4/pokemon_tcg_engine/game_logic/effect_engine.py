# pokemon_tcg_engine/game_logic/effect_engine.py
"""Handles the application of card effects, attack effects, abilities, status conditions, etc."""

import random # For coin flips
from typing import TYPE_CHECKING, Optional, List, Any

if TYPE_CHECKING:
    from ..game_state import GameState
    from ..cards.pokemon_card import PokemonCard, AttackData
    from ..cards.trainer_card import TrainerCard
    from ..game_elements.player_state import PlayerState
    from ..cards.card_enums import StatusCondition, PokemonType

class EffectEngine:
    """Applies various game effects triggered by cards or game events."""
    def __init__(self, game_state: "GameState"):
        self.game_state = game_state

    def flip_coin(self) -> bool:
        """Simulates a coin flip. Returns True for heads, False for tails."""
        result = random.choice([True, False])
        print(f"Coin flip: {"Heads" if result else "Tails"}")
        return result

    def apply_status_condition(self, target_pokemon: "PokemonCard", status: "StatusCondition"):
        """Applies a status condition to a Pokémon, respecting existing rules (e.g., cannot be Asleep and Paralyzed simultaneously)."""
        from ..cards.card_enums import StatusCondition # Local import

        # Rules for stacking/overwriting status conditions:
        # - Asleep, Paralyzed, Confused are mutually exclusive. Applying one cures the others.
        # - Poisoned and Burned can stack with each other and with one of Asleep/Paralyzed/Confused.
        
        current_major_statuses = {StatusCondition.ASLEEP, StatusCondition.PARALYZED, StatusCondition.CONFUSED}
        
        if status in current_major_statuses:
            for s in list(target_pokemon.status_conditions): # Iterate over a copy for modification
                if s in current_major_statuses and s != status:
                    target_pokemon.cure_status(s)
        
        target_pokemon.apply_status(status)
        # print(f"{target_pokemon.name} is now {status.name}.") # Already printed by PokemonCard.apply_status

    def resolve_status_effects_phase(self, player_whose_turn_is_ending: "PlayerState"):
        """Resolves effects of ongoing status conditions during the Between Turns Checks phase."""
        from ..cards.card_enums import StatusCondition # Local import

        print(f"Resolving status effects for {player_whose_turn_is_ending.name}'s Pokémon at end of their turn.")
        active_pokemon = player_whose_turn_is_ending.board.get_active_pokemon()

        if not active_pokemon:
            return

        # Handle statuses that prevent untapping or have effects before player action
        # (This is more for games like MtG; Pokémon statuses are mostly during checkup)

        # --- Pokémon Checkup (Between Turns) --- 
        # Order: Poison, Burn, Asleep, Paralyzed. (Confusion is checked before attack)

        if StatusCondition.POISONED in active_pokemon.status_conditions:
            print(f"{active_pokemon.name} takes 10 damage from Poison.")
            active_pokemon.take_damage(10) # No type on poison damage
            if active_pokemon.current_hp <= 0:
                self.game_state.action_resolver.handle_knock_out(player_whose_turn_is_ending, active_pokemon, prize_taker=self.game_state.get_opponent(player_whose_turn_is_ending))
                return # Stop further status checks if KO

        if StatusCondition.BURNED in active_pokemon.status_conditions:
            print(f"{active_pokemon.name} is Burned. Flipping a coin...")
            if self.flip_coin(): # Heads
                active_pokemon.cure_status(StatusCondition.BURNED)
                print(f"{active_pokemon.name} is no longer Burned.")
            else: # Tails
                print(f"{active_pokemon.name} takes 20 damage from Burn.")
                active_pokemon.take_damage(20) # No type on burn damage
                if active_pokemon.current_hp <= 0:
                    self.game_state.action_resolver.handle_knock_out(player_whose_turn_is_ending, active_pokemon, prize_taker=self.game_state.get_opponent(player_whose_turn_is_ending))
                    return # Stop further status checks if KO
        
        if StatusCondition.ASLEEP in active_pokemon.status_conditions:
            print(f"{active_pokemon.name} is Asleep. Flipping a coin to see if it wakes up...")
            if self.flip_coin(): # Heads
                active_pokemon.cure_status(StatusCondition.ASLEEP)
                print(f"{active_pokemon.name} woke up!")
            else: # Tails
                print(f"{active_pokemon.name} is still Asleep.")

        if StatusCondition.PARALYZED in active_pokemon.status_conditions:
            # Paralysis wears off at the end of the affected player's *next* turn.
            # So, if it was applied during opponent's turn, it wears off now.
            # This logic needs to be tied to when Paralysis was applied or a turn counter for the status.
            # For simplicity now: assume it wears off after one full turn cycle for the affected Pokémon.
            # A better way: add a flag `paralyzed_this_turn` or `paralyzed_until_end_of_next_turn`
            print(f"{active_pokemon.name} was Paralyzed. It is now cured.")
            active_pokemon.cure_status(StatusCondition.PARALYZED)

    def apply_attack_effect(self, attacking_pokemon: "PokemonCard", defending_pokemon: "PokemonCard", attack: "AttackData", attack_damage_done: int):
        """Applies any additional effects of an attack, beyond damage.
           This will become a large dispatcher based on attack.effect_description or a more structured effect system.
        """
        print(f"Applying effects for attack: {attack.name} from {attacking_pokemon.name} on {defending_pokemon.name}.")
        effect_text = attack.effect_description
        if not effect_text:
            return

        # This is where you would parse effect_text or have a library of predefined effect functions.
        # Example placeholder effects based on common Pokémon TCG patterns:

        if "poison" in effect_text.lower(): # Example: "Opponent's Active Pokémon is now Poisoned."
            print(f"Attack effect: Poisoning {defending_pokemon.name}.")
            self.apply_status_condition(defending_pokemon, StatusCondition.POISONED)
        
        if "burn" in effect_text.lower(): # Example: "Opponent's Active Pokémon is now Burned."
            print(f"Attack effect: Burning {defending_pokemon.name}.")
            self.apply_status_condition(defending_pokemon, StatusCondition.BURNED)

        if "paralyze" in effect_text.lower() or "paralyzed" in effect_text.lower():
            print(f"Attack effect: Paralyzing {defending_pokemon.name}.")
            self.apply_status_condition(defending_pokemon, StatusCondition.PARALYZED)

        if "asleep" in effect_text.lower() or "sleep" in effect_text.lower():
            print(f"Attack effect: Making {defending_pokemon.name} Asleep.")
            self.apply_status_condition(defending_pokemon, StatusCondition.ASLEEP)

        if "confuse" in effect_text.lower() or "confused" in effect_text.lower():
            print(f"Attack effect: Confusing {defending_pokemon.name}.")
            self.apply_status_condition(defending_pokemon, StatusCondition.CONFUSED)

        if "draw" in effect_text.lower() and "card" in effect_text.lower():
            # Example: "Draw 3 cards."
            num_cards_to_draw = self._parse_draw_cards_effect(effect_text)
            if num_cards_to_draw > 0:
                print(f"Attack effect: {attacking_pokemon.player.name} draws {num_cards_to_draw} cards.")
                # attacking_pokemon.player.draw_cards(num_cards_to_draw) # PlayerState needs this method
                pass # Placeholder for actual draw

        if "discard" in effect_text.lower() and "energy" in effect_text.lower():
            # Example: "Discard an Energy attached to the Defending Pokémon."
            # This requires target selection if multiple energies.
            print(f"Attack effect: Discarding energy from {defending_pokemon.name} (needs implementation).")
            # self.discard_energy_from_pokemon(defending_pokemon, 1)
            pass
        
        # ... many more effects ...

    def _parse_draw_cards_effect(self, effect_text: str) -> int:
        """Simple parser for 'Draw X cards' effects."""
        import re
        match = re.search(r"draw\s+(\d+)\s+card", effect_text.lower())
        if match:
            return int(match.group(1))
        return 0

    def apply_ability_effect(self, player_using_ability: "PlayerState", pokemon_with_ability: "PokemonCard", ability_name: str):
        """Applies the effect of a Pokémon's ability."""
        if not pokemon_with_ability.ability or pokemon_with_ability.ability.name != ability_name:
            print(f"Error: Ability {ability_name} not found on {pokemon_with_ability.name}.")
            return

        print(f"{player_using_ability.name} uses Ability: {pokemon_with_ability.ability.name} on {pokemon_with_ability.name} - {pokemon_with_ability.ability.description}")
        # Similar to attack effects, this will need a dispatcher or structured effect system.
        # Example: if ability_name == "Energy Trans": ...
        pass

    def apply_trainer_effect(self, player: "PlayerState", trainer_card: "TrainerCard", targets: Optional[List[Any]] = None):
        """Applies the effect of a Trainer card.
           This is the central dispatcher for Trainer card effects.
        """
        print(f"Applying effect for Trainer card: {trainer_card.name} played by {player.name}.")
        # This will become a large dispatcher based on trainer_card.name or card_id.
        # Example:
        # if trainer_card.name == "Potion":
        #     if targets and isinstance(targets[0], PokemonCard):
        #         target_pokemon = targets[0]
        #         print(f"Effect: Healing 30 damage from {target_pokemon.name}.")
        #         target_pokemon.heal(30)
        #     else:
        #         print("Error: Potion requires a target Pokémon.")
        # elif trainer_card.name == "Professor's Research":
        #     print(f"Effect: {player.name} discards their hand and draws 7 cards.")
        #     player.discard_hand()
        #     player.draw_cards(7)
        # ... many more trainer effects
        pass

    # More helper methods for specific types of effects:
    # - discard_energy_from_pokemon(target_pokemon, count, type_filter)
    # - search_deck_for_card(player, criteria_fn, num_to_take, show_to_opponent, add_to_hand)
    # - move_pokemon_to_bench(player, pokemon_to_move, from_zone)
    # - switch_active_pokemon(player, new_active_from_bench)

