# pokemon_tcg_engine/game_logic/turn_manager.py
"""Manages the game turns, phases, and player switching for Pokémon TCG Pocket."""

from enum import Enum, auto
from typing import TYPE_CHECKING, List  # Ajout de List ici

if TYPE_CHECKING:
    from ..game_state import GameState
    from ..game_elements.player_state import PlayerState

class GamePhase(Enum):
    # Pre-game phases
    SETUP_START = auto() # Initial game setup, before players place Pokémon
    SETUP_PLACE_POKEMON = auto() # Players place active and benched Pokémon
    SETUP_REVEAL_POKEMON = auto() # Pokémon are revealed
    SETUP_COMPLETE = auto() # Setup finished, ready for first turn

    # In-turn phases (based on rules.md)
    TURN_START = auto() # 1. Draw card, generate energy (except P1T1 for energy)
    MAIN_ACTIONS = auto() # 2-7. Place Pokémon, Attach Energy, Play Trainers, Evolve, Use Abilities, Retreat
    ATTACK = auto() # 8. Use an attack (ends the turn)
    
    # Post-turn/Between-turns phases
    BETWEEN_TURNS_CHECKS = auto() # Check KOs, apply status conditions, check win conditions
    GAME_OVER = auto()

class TurnManager:
    """Handles the flow of turns and phases within the Pokémon TCG Pocket game."""
    def __init__(self, game_state: "GameState"):
        self.game_state = game_state
        self.current_phase = GamePhase.SETUP_START
        self.turn_number = 0 # Increments when player 1 starts their turn
        self.player1_first_turn: bool = True # Special rule for P1T1 (no energy generation, no attack)

    def start_game_setup(self):
        """Initiates the game setup process."""
        print("Starting game setup...")
        self.current_phase = GamePhase.SETUP_START
        # Logic for coin flip to determine who goes first would be here or in GameState
        # For now, assume player1 is decided to go first by GameState
        # self.game_state.player1.setup_player_pre_game() # Shuffle deck, set prizes (no hand draw yet)
        # self.game_state.player2.setup_player_pre_game()
        print("Game setup started. Waiting for players to place Pokémon.")
        self.current_phase = GamePhase.SETUP_PLACE_POKEMON
        # The game would now wait for player actions to place Pokémon.

    def complete_pokemon_placement(self):
        """Called after both players have placed their initial Pokémon."""
        if self.current_phase != GamePhase.SETUP_PLACE_POKEMON:
            print(f"Error: Cannot complete Pokémon placement from phase {self.current_phase.name}")
            return
        print("Both players have placed Pokémon. Revealing Pokémon...")
        self.current_phase = GamePhase.SETUP_REVEAL_POKEMON
        # Reveal Pokémon logic (if any specific action is needed beyond them being on board)
        self.current_phase = GamePhase.SETUP_COMPLETE
        print("Setup complete. Ready to start the first turn.")
        self.start_first_turn()

    def start_first_turn(self):
        if self.current_phase != GamePhase.SETUP_COMPLETE:
            print(f"Error: Cannot start first turn from phase {self.current_phase.name}")
            return
        
        self.turn_number = 1
        self.player1_first_turn = True # Active player is P1 for the first turn
        # GameState should set active_player to player1
        # self.game_state.active_player.draw_initial_hand() # Draw initial hand for P1
        # self.game_state.inactive_player.draw_initial_hand() # Draw initial hand for P2
        print(f"Turn {self.turn_number} begins. Active player: {self.game_state.active_player.name}")
        self.transition_to_phase(GamePhase.TURN_START)

    def transition_to_phase(self, next_phase: GamePhase):
        """Handles the transition to a new phase and executes phase-start logic."""
        print(f"Transitioning from {self.current_phase.name} to {next_phase.name}")
        self.current_phase = next_phase
        active_player: "PlayerState" = self.game_state.active_player

        if self.current_phase == GamePhase.TURN_START:
            active_player.reset_turn_flags() # Reset supporter played, energy attached, etc.
            # 1. Draw a card
            # active_player.draw_cards(1)
            print(f"{active_player.name} draws a card.")
            # 1. Generate Energy (except P1T1)
            if not (self.game_state.active_player == self.game_state.player1 and self.player1_first_turn):
                # active_player.generate_energy_for_turn() # Needs implementation in PlayerState
                print(f"{active_player.name} generates energy.")
            else:
                print(f"{active_player.name} (Player 1, Turn 1) does not generate energy this turn.")
            self.transition_to_phase(GamePhase.MAIN_ACTIONS)

        elif self.current_phase == GamePhase.MAIN_ACTIONS:
            print(f"{active_player.name} is in Main Actions phase. Waiting for player input...")
            # Player can now: Place Pokémon, Attach Energy, Play Trainers, Evolve, Use Abilities, Retreat.
            # The game loop will wait for an action from the player (or AI).
            # If player chooses to attack, they trigger a transition to ATTACK phase.
            # If player chooses to end turn without attacking (if allowed), transition to BETWEEN_TURNS_CHECKS.
            pass

        elif self.current_phase == GamePhase.ATTACK:
            print(f"{active_player.name} is in Attack phase.")
            # ActionResolver handles the attack. After attack resolution:
            # active_player.has_attacked_this_turn = True (or similar flag)
            # Then, automatically transition to between turns checks.
            # For now, assume attack is resolved by ActionResolver, then we manually call end_attack_phase()
            pass # Waiting for attack to be chosen and resolved

        elif self.current_phase == GamePhase.BETWEEN_TURNS_CHECKS:
            print("Between Turns: Checking KOs, applying status effects, checking win conditions...")
            # self.game_state.effect_engine.resolve_status_effects_phase(active_player) # Apply poison, burn, check sleep/paralysis for recovery
            # self.game_state.check_knockouts_and_promote() # Handles KOs, prize taking, promoting new active
            
            winner = self.game_state.check_win_conditions()
            if winner:
                self.transition_to_phase(GamePhase.GAME_OVER)
            else:
                # If no winner, proceed to next player's turn
                self.game_state.switch_active_player()
                if self.game_state.active_player == self.game_state.player1:
                    self.turn_number += 1
                    self.player1_first_turn = False # No longer P1T1 after P1 completes their first turn
                
                print(f"Turn {self.turn_number} (for {self.game_state.active_player.name}) begins.")
                self.transition_to_phase(GamePhase.TURN_START)

        elif self.current_phase == GamePhase.GAME_OVER:
            print(f"Game Over! Winner: {self.game_state.winner.name if self.game_state.winner else 'None determined'}")
            # Further cleanup or logging can happen here.

    def player_chooses_to_attack(self):
        """Called by game logic when the active player decides to initiate an attack."""
        if self.current_phase == GamePhase.MAIN_ACTIONS:
            # Player 1 on their first turn cannot attack (common TCG rule, check if in Pocket rules.md explicitly)
            # rules.md: "Début du tour : Piochez une carte et générez de l’Énergie (sauf au premier tour)." - doesn't explicitly forbid P1T1 attack.
            # However, most Pokémon TCGs have this rule. For now, let's assume it's allowed unless specified.
            self.transition_to_phase(GamePhase.ATTACK)
        else:
            print(f"Error: Cannot choose to attack from phase {self.current_phase.name}")

    def end_attack_phase_and_turn(self):
        """Called after an attack is fully resolved, or if player ends turn after attack phase."""
        if self.current_phase == GamePhase.ATTACK:
            self.transition_to_phase(GamePhase.BETWEEN_TURNS_CHECKS)
        else:
            print(f"Error: Cannot end attack phase from {self.current_phase.name}")

    def player_ends_main_actions_without_attacking(self):
        """Called if a player chooses to end their turn during MAIN_ACTIONS without attacking."""
        # This might be allowed or not depending on specific game rules (usually an attack ends the turn).
        # Pokémon TCG Pocket rules.md: "Utiliser une attaque : Lancez une attaque avec le Pokémon Actif pour terminer le tour."
        # This implies an attack IS the way to end the turn. So this method might not be used.
        if self.current_phase == GamePhase.MAIN_ACTIONS:
            print(f"{self.game_state.active_player.name} ends their turn without attacking.")
            self.transition_to_phase(GamePhase.BETWEEN_TURNS_CHECKS)
        else:
            print(f"Error: Cannot end main actions from phase {self.current_phase.name}")

    def get_current_phase_actions(self) -> List[str]:
        """Returns a list of valid high-level actions for the current player in the current phase."""
        # This will be crucial for the AI agent and for validating player input.
        actions = []
        if self.current_phase == GamePhase.SETUP_PLACE_POKEMON:
            actions.extend(["place_basic_pokemon_active", "place_basic_pokemon_bench", "confirm_placement"])
        elif self.current_phase == GamePhase.MAIN_ACTIONS:
            actions.extend(["play_pokemon_from_hand", "attach_energy_to_pokemon", 
                            "play_trainer_card", "evolve_pokemon", "use_ability", 
                            "retreat_pokemon", "initiate_attack"])
        elif self.current_phase == GamePhase.ATTACK:
            # Active Pokémon's available attacks
            active_pkmn = self.game_state.active_player.board.get_active_pokemon()
            if active_pkmn:
                for attack in active_pkmn.attacks:
                    # if active_pkmn.can_afford_attack(attack.name): # Rule check needed
                    actions.append(f"use_attack_{attack.name.replace(' ', '_').lower()}")
            actions.append("cancel_attack_choice") # Go back to MAIN_ACTIONS if allowed
        # Add more based on phase
        return actions

