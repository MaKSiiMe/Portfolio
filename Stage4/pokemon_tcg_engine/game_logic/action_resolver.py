# pokemon_tcg_engine/game_logic/action_resolver.py
"""Handles the resolution of player actions and their effects on the game state."""

from typing import TYPE_CHECKING, Optional, List, Any

if TYPE_CHECKING:
    from ..game_state import GameState
    from ..cards.base_card import BaseCard
    from ..cards.pokemon_card import PokemonCard, Attack
    from ..cards.trainer_card import TrainerCard, SupporterCard, ItemCard, StadiumCard, ToolCard, FossilCard
    from ..cards.card_enums import PokemonType, TrainerType
    from ..game_elements.player_state import PlayerState
    from .rule_checks import RuleChecks
    from .turn_manager import GamePhase

class ActionResolver:
    """Resolves actions taken by players, such as playing cards or attacking."""
    def __init__(self, game_state: "GameState", rule_checker: "RuleChecks"):
        self.game_state = game_state
        self.rule_checker = rule_checker

    def resolve_play_pokemon_card_action(
        self,
        player: "PlayerState", 
        pokemon_card: "PokemonCard", 
        to_active: bool = False, # True if trying to play directly to active (e.g. initial setup or after KO)
        bench_slot_index: Optional[int] = None, # Specify bench slot if needed, otherwise first available
        evolution_target: Optional["PokemonCard"] = None # The Pokémon to evolve
    ) -> bool:
        """Resolves playing a Pokémon card from hand to bench or evolving an existing Pokémon."""
        from ..cards.pokemon_card import EvolutionStage # Local import

        if not self.rule_checker.can_play_pokemon_card(player, pokemon_card, to_active, bench_slot_index, evolution_target):
            # Error message already printed by rule_checker
            return False

        if not player.remove_card_from_hand(pokemon_card):
            print(f"Error: Card {pokemon_card.name} could not be removed from {player.name}'s hand (should not happen if rule check passed).")
            return False # Should be caught by rule_checker if card not in hand

        print(f"Player {player.name} plays {pokemon_card.name}.")

        if pokemon_card.evolution_stage == EvolutionStage.BASIC:
            if to_active: # Usually for setup or replacing a KO'd active Pokémon
                if player.board.place_on_active(pokemon_card):
                    pokemon_card.turns_in_play = 0 # Just played
                    return True
            else: # Play to bench
                if player.board.add_to_bench(pokemon_card):
                    pokemon_card.turns_in_play = 0 # Just played
                    return True
        elif pokemon_card.evolution_stage in [EvolutionStage.STAGE_1, EvolutionStage.STAGE_2]:
            if evolution_target:
                # Remove the base Pokémon from play (it becomes part of the evolution stack)
                # The evolution_card (e.g., Charizard) replaces the evolution_target (e.g., Charmeleon) on the board.
                # Energies and other attached cards usually transfer.
                
                # Find where the evolution_target is (active or bench)
                is_target_active = player.board.get_active_pokemon() == evolution_target
                target_bench_index = -1
                if not is_target_active:
                    try:
                        target_bench_index = player.board.get_bench_pokemon().index(evolution_target)
                    except ValueError:
                        print(f"Error: Evolution target {evolution_target.name} not found on bench.")
                        player.add_card_to_hand(pokemon_card) # Return card to hand
                        return False

                # Transfer state (energies, damage, tool, status) from base to evolution
                pokemon_card.current_hp = pokemon_card.hp - (evolution_target.hp - evolution_target.current_hp) # Transfer damage
                pokemon_card.attached_energies = evolution_target.attached_energies.copy()
                pokemon_card.status_conditions = evolution_target.status_conditions.copy()
                pokemon_card.pokemon_tool_attached = evolution_target.pokemon_tool_attached
                if pokemon_card.pokemon_tool_attached:
                    # If tool has on_attach effect, it might need re-evaluation or not.
                    # For simplicity, assume tool stays and its effects continue if passive.
                    pass 
                pokemon_card.turns_in_play = evolution_target.turns_in_play # Evolution continues turns in play count

                # Place the evolution card
                if is_target_active:
                    player.board.remove_from_active() # Remove base
                    player.board.place_on_active(pokemon_card) # Place evolution
                else:
                    player.board.bench[target_bench_index] = pokemon_card # Replace in bench slot
                    evolution_target.is_benched = False # Old card no longer on bench
                    pokemon_card.is_benched = True
                
                player.add_card_to_discard(evolution_target) # Base Pokémon card goes to discard (or under evolution)
                                                            # Standard TCG puts it under. Pocket rules might differ.
                                                            # For now, let's assume discard for simplicity of board state.
                print(f"{evolution_target.name} evolved into {pokemon_card.name}.")
                return True
            else:
                print("Error: Evolution target not provided for evolution card.") # Should be caught by rule_checker
                player.add_card_to_hand(pokemon_card) # Return card to hand
                return False
        
        # If action failed for some reason, return card to hand
        player.add_card_to_hand(pokemon_card)
        return False

    def resolve_play_trainer_card_action(self, player: "PlayerState", trainer_card: "TrainerCard", targets: Optional[List[Any]] = None) -> bool:
        """Resolves playing a Trainer card from hand."""
        from ..cards.trainer_card import TrainerType, SupporterCard, ToolCard, FossilCard, StadiumCard # Local import

        if not self.rule_checker.can_play_trainer_card(player, trainer_card, targets[0] if targets else None):
            return False

        if not player.remove_card_from_hand(trainer_card):
            print(f"Error: Card {trainer_card.name} could not be removed from {player.name}'s hand.")
            return False

        print(f"Player {player.name} plays {trainer_card.name} ({trainer_card.trainer_type.name}).")

        # Apply card effect - this will be expanded in EffectEngine or specific card methods
        # trainer_card.play_effect(player, targets) # Assuming card has its own effect logic for now
        # For now, just print and handle basic state changes
        self.game_state.effect_engine.apply_trainer_effect(player, trainer_card, targets)

        if isinstance(trainer_card, SupporterCard):
            player.has_played_supporter_this_turn = True
        
        if isinstance(trainer_card, ToolCard):
            if targets and isinstance(targets[0], PokemonCard):
                target_pokemon = targets[0]
                target_pokemon.pokemon_tool_attached = trainer_card
                # trainer_card.on_attach(target_pokemon) # Tool card applies its on-attach effect
                print(f"Tool {trainer_card.name} attached to {target_pokemon.name}.")
                # Tool stays in play, does not go to discard immediately
                return True 
            else:
                print(f"Error: Tool card {trainer_card.name} played without a valid Pokémon target.")
                player.add_card_to_hand(trainer_card) # Return to hand
                return False
        elif isinstance(trainer_card, StadiumCard):
            # self.game_state.global_board.set_active_stadium(trainer_card, player.board if self.game_state.global_board.active_stadium else None)
            # Stadium stays in play
            print(f"Stadium {trainer_card.name} is now active.")
            return True
        elif isinstance(trainer_card, FossilCard):
            # FossilCard's play_effect should handle placing the Pokémon on bench
            # and then the Fossil card itself is usually discarded.
            # trainer_card.play_effect(player) # This was already called by effect_engine
            player.add_card_to_discard(trainer_card)
            return True
        
        # Most other trainers (Items, Supporters after effect) go to discard
        if trainer_card.trainer_type not in [TrainerType.TOOL, TrainerType.STADIUM]: # Tools and Stadiums stay
            player.add_card_to_discard(trainer_card)
        
        return True

    def resolve_attach_energy_action(self, player: "PlayerState", pokemon_target: "PokemonCard", energy_type: "PokemonType", count: int = 1) -> bool:
        """Resolves attaching a generated energy to a Pokémon."""
        if not self.rule_checker.can_attach_energy(player, pokemon_target, energy_type):
            return False

        if player.available_energies.get(energy_type, 0) >= count:
            player.available_energies[energy_type] -= count
            pokemon_target.attach_energy_type(energy_type, count)
            player.has_attached_energy_this_turn = True
            print(f"{count} {energy_type.name} energy attached to {pokemon_target.name} by {player.name}.")
            return True
        else:
            print(f"Error: Player {player.name} does not have enough {energy_type.name} energy. (Should be caught by rule_checker)")
            return False

    def resolve_retreat_action(self, player: "PlayerState", pokemon_to_promote: "PokemonCard") -> bool:
        """Resolves a player retreating their active Pokémon to the bench."""
        if not self.rule_checker.can_retreat(player, pokemon_to_promote):
            return False

        active_pokemon = player.board.get_active_pokemon()
        if not active_pokemon: return False # Should be caught by rules

        # Pay retreat cost (discard specified number of energies from active_pokemon)
        # This needs a mechanism for the player to choose which energies to discard if there are multiple types.
        # For now, assume any `active_pokemon.retreat_cost` energies are discarded.
        # A more robust implementation would involve `player.choose_energies_to_discard(active_pokemon, active_pokemon.retreat_cost)`
        energies_to_discard_count = active_pokemon.retreat_cost
        detached_count = 0
        temp_attached_energies = active_pokemon.attached_energies.copy() # Iterate over a copy
        
        # Simplistic discard: prefer colorless if possible, then any type. This needs refinement.
        # For now, just check if total count is enough, actual discard logic is complex.
        # We'll just remove `retreat_cost` worth of arbitrary energy for this placeholder.
        for energy_type_on_card, num in temp_attached_energies.items():
            if detached_count >= energies_to_discard_count:
                break
            can_detach = min(num, energies_to_discard_count - detached_count)
            active_pokemon.detach_energy_type(energy_type_on_card, can_detach)
            # player.add_energy_to_discard_pool(energy_type_on_card, can_detach) # Or energies go to discard pile as cards if they were cards
            # Since energies are generated, detaching might just make them vanish or return to a general pool.
            # For now, assume they vanish from the Pokémon.
            print(f"Detached {can_detach} {energy_type_on_card.name} energy from {active_pokemon.name} for retreat.")
            detached_count += can_detach
        
        if detached_count < energies_to_discard_count:
            print(f"Error: Could not detach enough energy for retreat (should be caught by rule check or choice mechanism).")
            # Rollback or error state - this part needs careful handling of energy choice.
            return False

        # Perform the swap
        player.board.remove_from_active()
        player.board.promote_from_bench_to_active(pokemon_to_promote)
        player.board.add_to_bench(active_pokemon) # The retreated Pokémon goes to the bench
        
        active_pokemon.status_conditions.clear() # Retreating cures most status conditions
        print(f"{active_pokemon.name} retreated to bench. {pokemon_to_promote.name} is now active.")
        player.has_retreated_this_turn = True
        return True

    def resolve_attack_action(self, attacking_player: "PlayerState", chosen_attack_name: str) -> bool:
        """Resolves a Pokémon attacking the opponent's active Pokémon."""
        from ..cards.card_enums import StatusCondition # Local import

        active_player = self.game_state.active_player
        if attacking_player != active_player:
            print(f"Error: It is not player {attacking_player.name}'s turn to attack.")
            return False

        attacker_pokemon = attacking_player.board.get_active_pokemon()
        if not attacker_pokemon:
            print(f"Error: Player {attacking_player.name} has no active Pokémon.")
            return False

        attack_to_use = next((atk for atk in attacker_pokemon.attacks if atk.name == chosen_attack_name), None)
        if not attack_to_use:
            print(f"Error: Attack {chosen_attack_name} not found for {attacker_pokemon.name}.")
            return False

        if not self.rule_checker.can_attack(attacking_player, attacker_pokemon, attack_to_use):
            return False
        
        if StatusCondition.CONFUSED in attacker_pokemon.status_conditions:
            print(f"{attacker_pokemon.name} is Confused! Flipping a coin to see if attack succeeds...")
            if self.game_state.effect_engine.flip_coin(): # True for Heads (attack succeeds)
                print("Coin is Heads! Attack proceeds.")
            else: # Tails (attack fails, Pokémon damages itself)
                print("Coin is Tails! Attack fails. {attacker_pokemon.name} takes 30 damage from confusion.")
                attacker_pokemon.take_damage(30) # Standard confusion self-damage
                # Check if attacker KO'd itself
                if attacker_pokemon.current_hp <= 0:
                    self.handle_knock_out(attacking_player, attacker_pokemon)
                self.game_state.turn_manager.end_attack_phase_and_turn()
                return True # Attack action resolved (even if it failed due to confusion)

        print(f"{attacker_pokemon.name} uses {attack_to_use.name}!")

        opponent = self.game_state.get_opponent(attacking_player)
        defender_pokemon = opponent.board.get_active_pokemon()

        if not defender_pokemon:
            print(f"Opponent {opponent.name} has no active Pokémon to defend. This might be a win condition.")
            # GameState should check win conditions after this phase
            self.game_state.turn_manager.end_attack_phase_and_turn()
            return True 

        # 1. Apply attack damage
        damage_done = defender_pokemon.take_damage(attack_to_use.damage, attacker_pokemon.pokemon_type)
        print(f"{defender_pokemon.name} takes {damage_done} damage from {attack_to_use.name}.")

        # 2. Apply attack effects (handled by EffectEngine)
        self.game_state.effect_engine.apply_attack_effect(attacker_pokemon, defender_pokemon, attack_to_use, damage_done)

        # 3. Check for KOs
        if defender_pokemon.current_hp <= 0:
            self.handle_knock_out(opponent, defender_pokemon, prize_taker=attacking_player)
        
        # Check for self-inflicted KO or recoil from effects
        if attacker_pokemon.current_hp <= 0:
            self.handle_knock_out(attacking_player, attacker_pokemon, prize_taker=opponent)

        # Attacker has now attacked
        attacker_pokemon.has_attacked_this_turn = True # Or a global flag in PlayerState for the turn
        self.game_state.turn_manager.end_attack_phase_and_turn()
        return True

    def handle_knock_out(self, owner_of_koed_pokemon: "PlayerState", koed_pokemon: "PokemonCard", prize_taker: Optional["PlayerState"] = None):
        """Handles the process when a Pokémon is Knocked Out."""
        print(f"{koed_pokemon.name} belonging to {owner_of_koed_pokemon.name} is Knocked Out!")
        
        # Move KO'd Pokémon and its attachments to discard pile
        owner_of_koed_pokemon.add_card_to_discard(koed_pokemon)
        if koed_pokemon.pokemon_tool_attached:
            owner_of_koed_pokemon.add_card_to_discard(koed_pokemon.pokemon_tool_attached)
            koed_pokemon.pokemon_tool_attached = None
        # Attached energies (since they are generated, they might just vanish or go to a conceptual discard)
        # For now, assume they vanish with the Pokémon from play.
        koed_pokemon.attached_energies.clear()

        if owner_of_koed_pokemon.board.get_active_pokemon() == koed_pokemon:
            owner_of_koed_pokemon.board.remove_from_active()
        else:
            owner_of_koed_pokemon.board.remove_from_bench(koed_pokemon)

        # Prize taking
        if prize_taker:
            num_prizes = 2 if koed_pokemon.is_ex else 1
            for _ in range(num_prizes):
                prize_card = prize_taker.take_prize_card()
                if prize_card:
                    print(f"{prize_taker.name} took a prize card: {prize_card.name}")
                else:
                    print(f"{prize_taker.name} has no more prize cards to take (should be game over).")
                    break # Should be caught by win condition check
        
        # Owner of KO'd Pokémon must promote a new active Pokémon if their active was KO'd
        if owner_of_koed_pokemon.board.get_active_pokemon() is None and owner_of_koed_pokemon.board.get_bench_pokemon():
            print(f"{owner_of_koed_pokemon.name} must promote a new active Pokémon.")
            # Game logic will need to pause and wait for player input here.
            # For AI, this would be another decision point.
            # For now, this is a placeholder for that interaction.
        elif owner_of_koed_pokemon.board.get_active_pokemon() is None and not owner_of_koed_pokemon.board.get_bench_pokemon():
            print(f"{owner_of_koed_pokemon.name} has no Pokémon left in play! This might be a win condition for the opponent.")
            # GameState will check this win condition.

    # Add more resolver methods for other actions (using abilities, etc.)

