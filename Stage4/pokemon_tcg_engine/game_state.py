# pokemon_tcg_engine/game_state.py
"""Represents the overall state of a Pokémon TCG game session."""

from typing import Optional, List

from .game_elements.player_state import PlayerState
from .game_elements.board import GlobalBoardState # For shared elements like Stadium
# from .game_logic.turn_manager import TurnManager # Forward declaration or careful import
# from .game_logic.action_resolver import ActionResolver
# from .game_logic.effect_engine import EffectEngine
# from .game_logic.rule_checks import RuleChecks
# from lemon_tcg_lib.lemon_tcg.entities.game_state import GameState as LemonGameState # If using

class GameState:
    """Manages the entire state of the game, including players, board, and game flow."""
    def __init__(self, player1_deck: List[object], player2_deck: List[object], player1_name: str = "Player1", player2_name: str = "Player2"):
        self.player1 = PlayerState(player_id="p1", name=player1_name, deck_list=player1_deck)
        self.player2 = PlayerState(player_id="p2", name=player2_name, deck_list=player2_deck)
        self.global_board = GlobalBoardState() # For stadium, etc.
        
        self.active_player: Optional[PlayerState] = None
        self.inactive_player: Optional[PlayerState] = None # Convenience reference
        self.winner: Optional[PlayerState] = None

        # These will be initialized later to avoid circular dependencies if they need GameState
        # self.turn_manager = TurnManager(self) 
        # self.rule_checker = RuleChecks(self)
        # self.action_resolver = ActionResolver(self, self.rule_checker)
        # self.effect_engine = EffectEngine(self)
        
        self.game_started: bool = False
        print("GameState initialized.")

    def initialize_game_components(self, TurnManagerClass, RuleChecksClass, ActionResolverClass, EffectEngineClass):
        """Initializes components that require a GameState instance."""
        self.turn_manager = TurnManagerClass(self)
        self.rule_checker = RuleChecksClass(self)
        self.action_resolver = ActionResolverClass(self, self.rule_checker)
        self.effect_engine = EffectEngineClass(self)
        print("Game components (TurnManager, RuleChecks, ActionResolver, EffectEngine) initialized.")

    def start_game_flow(self):
        """Starts the actual game flow after setup."""
        if not hasattr(self, 'turn_manager') or not self.turn_manager:
            raise RuntimeError("TurnManager not initialized. Call initialize_game_components first.")
        self.player1.setup_player()
        self.player2.setup_player()
        # Decide who goes first (e.g., coin flip)
        # For now, player1 goes first
        self.set_active_player(self.player1)
        self.game_started = True
        self.turn_manager.start_game() # This will trigger the first phase

    def set_active_player(self, player: PlayerState):
        """Sets the active player and updates the inactive player reference."""
        self.active_player = player
        if player == self.player1:
            self.inactive_player = self.player2
        else:
            self.inactive_player = self.player1
        print(f"Active player is now: {self.active_player.name}")

    def switch_active_player(self):
        """Switches the active player."""
        if self.active_player == self.player1:
            self.set_active_player(self.player2)
        else:
            self.set_active_player(self.player1)

    def get_opponent(self, player: PlayerState) -> PlayerState:
        """Returns the opponent of the given player."""
        return self.player2 if player == self.player1 else self.player1

    def check_win_conditions(self) -> Optional[PlayerState]:
        """Checks if any player has met a win condition."""
        # Condition 1: A player has no prize cards left.
        if not self.player1.prize_cards:
            self.winner = self.player1
            return self.player1
        if not self.player2.prize_cards:
            self.winner = self.player2
            return self.player2

        # Condition 2: Opponent has no Pokémon in play (active or benched).
        # This check is usually done at the start of a player's turn if they need to promote an active Pokémon.
        # Or when a Pokémon is knocked out and no replacement can be promoted.
        # For simplicity, let's assume this is checked by TurnManager or ActionResolver.

        # Condition 3: A player cannot draw a card from their deck when required to.
        # This is usually checked when a player attempts to draw (e.g., at start of turn, or by card effect).
        
        return None

    def get_full_game_state_representation(self, perspective_player: Optional[PlayerState] = None) -> dict:
        """Returns a dictionary representation of the game state, 
           optionally from the perspective of a specific player (hiding opponent's hand)."""
        # This will be crucial for the Gym environment's observation space.
        state_representation = {
            "player1": {
                "name": self.player1.name,
                "hand_size": len(self.player1.hand),
                "deck_size": len(self.player1.deck),
                "discard_size": len(self.player1.discard_pile),
                "prize_cards_left": len(self.player1.prize_cards),
                "active_pokemon": self.player1.board.active_pokemon.name if self.player1.board.active_pokemon else None,
                "bench_size": len(self.player1.board.bench),
                # Add more details: specific cards on bench, energies, status, etc.
            },
            "player2": {
                "name": self.player2.name,
                "hand_size": len(self.player2.hand),
                "deck_size": len(self.player2.deck),
                "discard_size": len(self.player2.discard_pile),
                "prize_cards_left": len(self.player2.prize_cards),
                "active_pokemon": self.player2.board.active_pokemon.name if self.player2.board.active_pokemon else None,
                "bench_size": len(self.player2.board.bench),
            },
            "active_player_id": self.active_player.player_id if self.active_player else None,
            "current_phase": self.turn_manager.current_phase.name if hasattr(self, 'turn_manager') and self.turn_manager else None,
            "turn_number": self.turn_manager.turn_number if hasattr(self, 'turn_manager') and self.turn_manager else 0,
            "active_stadium": self.global_board.active_stadium.name if self.global_board.active_stadium else None,
            "winner": self.winner.name if self.winner else None
        }
        # If perspective_player is provided, you might want to include their actual hand cards
        # and hide the opponent's hand details beyond size.
        return state_representation

    def __str__(self) -> str:
        return f"Game State: Active Player - {self.active_player.name if self.active_player else 'None'}, Phase - {self.turn_manager.current_phase.name if hasattr(self, 'turn_manager') and self.turn_manager else 'N/A'}"

