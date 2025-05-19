# pokemon_tcg_engine/game_logic/rule_checks.py
"""Contains functions to check the validity of game actions based on Pokémon TCG rules."""

from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from ..game_state import GameState
    from ..cards.base_card import BaseCard
    from ..cards.pokemon_card import PokemonCard, Attack, EvolutionStage
    from ..cards.trainer_card import TrainerCard, SupporterCard, ToolCard, TrainerType
    from ..game_elements.player_state import PlayerState
    from .turn_manager import GamePhase

class RuleChecks:
    """Provides methods to validate game actions against established rules."""
    def __init__(self, game_state: "GameState"):
        self.game_state = game_state

    def _is_player_turn_and_phase(self, player: "PlayerState", expected_phase: "GamePhase") -> bool:
        """Helper to check if it is the player's turn and the correct game phase."""
        if self.game_state.active_player != player:
            print(f"Rule Error: It is not player {player.name}'s turn.")
            return False
        if self.game_state.turn_manager.current_phase != expected_phase:
            print(f"Rule Error: Action not allowed in phase {self.game_state.turn_manager.current_phase.name}. Expected {expected_phase.name}.")
            return False
        return True

    def can_play_pokemon_card(self, player: "PlayerState", pokemon_card: "PokemonCard", to_active: bool, bench_slot_index: Optional[int] = None, evolution_target: Optional["PokemonCard"] = None) -> bool:
        """Checks if the player can legally play the given Pokémon card from hand."""
        from .turn_manager import GamePhase # Local import for enum
        from ..cards.pokemon_card import EvolutionStage # Local import for enum

        if not self._is_player_turn_and_phase(player, GamePhase.MAIN_ACTIONS):
            return False

        if pokemon_card not in player.hand:
            print(f"Rule Error: Card {pokemon_card.name} is not in player {player.name}'s hand.")
            return False

        if pokemon_card.evolution_stage == EvolutionStage.BASIC:
            if to_active:
                if player.board.get_active_pokemon() is not None:
                    # This case is usually for initial setup or if active is KO'd. 
                    # During MAIN_ACTIONS, you usually play to bench first or evolve.
                    print(f"Rule Error: Cannot play Basic Pokémon {pokemon_card.name} directly to active if active slot is occupied during Main Actions.")
                    return False 
            else: # Playing to bench
                if player.board.is_bench_full():
                    print(f"Rule Error: Bench is full. Cannot play {pokemon_card.name}.")
                    return False
        elif pokemon_card.evolution_stage in [EvolutionStage.STAGE_1, EvolutionStage.STAGE_2]: # Evolution
            if not evolution_target:
                print(f"Rule Error: Evolution target must be specified for {pokemon_card.name}.")
                return False
            if not pokemon_card.can_evolve_from(evolution_target.name):
                print(f"Rule Error: {pokemon_card.name} cannot evolve from {evolution_target.name}.")
                return False
            if evolution_target.turns_in_play < 1 and not (self.game_state.turn_manager.player1_first_turn and self.game_state.active_player == self.game_state.player1):
                 # Cannot evolve on the first turn the Pokémon was played or on P1T1 for that Pokémon
                 # Exception: some card effects might allow this.
                print(f"Rule Error: Cannot evolve {evolution_target.name} on its first turn in play or during P1T1 for that Pokémon.")
                return False
            if evolution_target not in player.board.get_all_pokemon_in_play():
                print(f"Rule Error: Evolution target {evolution_target.name} is not in play for player {player.name}.")
                return False
        else:
            print(f"Rule Error: Unknown evolution stage for {pokemon_card.name}.")
            return False
        
        print(f"Rule check passed for playing {pokemon_card.name}.")
        return True

    def can_play_trainer_card(self, player: "PlayerState", trainer_card: "TrainerCard", target: Optional[Any] = None) -> bool:
        """Checks if the player can legally play the given Trainer card."""
        from .turn_manager import GamePhase # Local import for enum
        from ..cards.trainer_card import TrainerType # Local import for enum

        if not self._is_player_turn_and_phase(player, GamePhase.MAIN_ACTIONS):
            return False

        if trainer_card not in player.hand:
            print(f"Rule Error: Card {trainer_card.name} is not in player {player.name}'s hand.")
            return False

        if trainer_card.trainer_type == TrainerType.SUPPORTER and player.has_played_supporter_this_turn:
            print("Rule Error: Already played a Supporter this turn.")
            return False
        
        if trainer_card.trainer_type == TrainerType.TOOL:
            if not target or not hasattr(target, 'pokemon_tool_attached'): # Check if target is a Pokémon
                print("Rule Error: Pokémon Tool must target a Pokémon.")
                return False
            if target.pokemon_tool_attached is not None:
                print(f"Rule Error: {target.name} already has a Pokémon Tool attached.")
                return False
        
        # Add specific checks for Item, Stadium if needed (e.g., can this stadium be played?)
        print(f"Rule check passed for playing {trainer_card.name}.")
        return True

    def can_attach_energy(self, player: "PlayerState", pokemon_target: "PokemonCard", energy_type_to_attach: "PokemonType") -> bool:
        """Checks if the player can attach an energy of the specified type to the target Pokémon."""
        from .turn_manager import GamePhase # Local import for enum

        if not self._is_player_turn_and_phase(player, GamePhase.MAIN_ACTIONS):
            return False
        
        if player.has_attached_energy_this_turn:
            print("Rule Error: Already attached energy this turn.")
            return False

        if pokemon_target not in player.board.get_all_pokemon_in_play():
            print(f"Rule Error: Target Pokémon {pokemon_target.name} is not in play for player {player.name}.")
            return False

        # Check if player has the specified energy type available (from generated pool)
        if player.available_energies.get(energy_type_to_attach, 0) < 1:
            print(f"Rule Error: Player {player.name} does not have {energy_type_to_attach.name} energy available to attach.")
            return False

        print(f"Rule check passed for attaching {energy_type_to_attach.name} energy to {pokemon_target.name}.")
        return True

    def can_attack(self, player: "PlayerState", attacking_pokemon: "PokemonCard", attack: "Attack") -> bool:
        """Checks if the Pokémon can legally perform the chosen attack."""
        from .turn_manager import GamePhase # Local import for enum
        from ..cards.card_enums import StatusCondition # Local import for enum

        # Attack happens in ATTACK phase, but decision might be made at end of MAIN_ACTIONS
        if not (self._is_player_turn_and_phase(player, GamePhase.MAIN_ACTIONS) or 
                self._is_player_turn_and_phase(player, GamePhase.ATTACK)):
            return False
        
        if player.board.get_active_pokemon() != attacking_pokemon:
            print(f"Rule Error: Attacking Pokémon {attacking_pokemon.name} is not active.")
            return False
        
        if StatusCondition.ASLEEP in attacking_pokemon.status_conditions or \
           StatusCondition.PARALYZED in attacking_pokemon.status_conditions:
            print(f"Rule Error: {attacking_pokemon.name} cannot attack due to being {next(iter(attacking_pokemon.status_conditions)).name}.")
            return False

        if not attacking_pokemon.can_afford_attack(attack.name):
            print(f"Rule Error: {attacking_pokemon.name} does not have enough energy for {attack.name}.")
            return False
        
        # Pokémon TCG Pocket rules.md does not explicitly forbid P1T1 attack.
        # Standard TCG often does. If this rule applies to Pocket, add check here:
        # if self.game_state.turn_manager.player1_first_turn and self.game_state.active_player == self.game_state.player1:
        #     print("Rule Error: Player 1 cannot attack on the first turn of the game.")
        #     return False

        print(f"Rule check passed for {attacking_pokemon.name} using {attack.name}.")
        return True

    def can_retreat(self, player: "PlayerState", pokemon_to_promote_to_active: "PokemonCard") -> bool:
        """Checks if the player can legally retreat their active Pokémon."""
        from .turn_manager import GamePhase # Local import for enum

        if not self._is_player_turn_and_phase(player, GamePhase.MAIN_ACTIONS):
            return False

        active_pokemon = player.board.get_active_pokemon()
        if not active_pokemon:
            print("Rule Error: No active Pokémon to retreat.")
            return False

        if player.has_retreated_this_turn:
            print("Rule Error: Already retreated this turn.")
            return False
        
        if not player.board.get_bench_pokemon():
            print("Rule Error: No Pokémon on the bench to promote.")
            return False
            
        if pokemon_to_promote_to_active not in player.board.get_bench_pokemon():
            print(f"Rule Error: {pokemon_to_promote_to_active.name} is not a valid Pokémon on the bench to promote.")
            return False

        # Check if player can pay the retreat cost (discard energies from active Pokémon)
        # This is complex as it involves selecting which energies to discard.
        # For now, assume a simple check of total energy count vs retreat cost.
        # A more robust check would ensure specific types can be discarded if costs are typed.
        total_attached_energy_count = sum(active_pokemon.attached_energies.values())
        if total_attached_energy_count < active_pokemon.retreat_cost:
            print(f"Rule Error: {active_pokemon.name} does not have enough energy ({total_attached_energy_count}) to pay retreat cost of {active_pokemon.retreat_cost}.")
            return False

        print(f"Rule check passed for retreating {active_pokemon.name}.")
        return True

    # Add more rule checking methods as needed (using abilities, etc.)

