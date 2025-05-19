# main.py
"""Main entry point for running or testing the Pokémon TCG engine."""

from pokemon_tcg_engine.game_state import GameState
from pokemon_tcg_engine.game_logic.turn_manager import TurnManager
from pokemon_tcg_engine.game_logic.rule_checks import RuleChecks
from pokemon_tcg_engine.game_logic.effect_engine import EffectEngine
from pokemon_tcg_engine.cards.pokemon_card import PokemonCard, Attack
from pokemon_tcg_engine.cards.card_enums import PokemonType, EvolutionStage

def run_simple_game_simulation():
    """Simulates a very basic game flow. For demonstration and early testing."""
    print("Starting a simple game simulation...")

    # 1. Create dummy Pokémon cards
    attack1 = Attack(name="Tackle", cost={PokemonType.COLORLESS: 1}, damage=10)
    attack2 = Attack(name="Ember", cost={PokemonType.FIRE: 1}, damage=30)
    bulbasaur = PokemonCard(
        card_id="001", name="Bulbasaur", hp=60, pokemon_type=PokemonType.GRASS,
        evolution_stage=EvolutionStage.BASIC, attacks=[attack1]
    )
    charmander = PokemonCard(
        card_id="004", name="Charmander", hp=50, pokemon_type=PokemonType.FIRE,
        evolution_stage=EvolutionStage.BASIC, attacks=[attack2]
    )

    # 2. Create decks for both players
    player1_deck = [bulbasaur] * 10
    player2_deck = [charmander] * 10

    # 3. Initialize GameState
    game = GameState(player1_deck=player1_deck, player2_deck=player2_deck)
    game.initialize_game_components(TurnManager, RuleChecks, None, EffectEngine)

    # 4. Start the game
    game.start_game_flow()

    # 5. Basic game loop
    max_turns = 10
    for turn in range(max_turns):
        if game.winner:
            print(f"Winner: {game.winner.name}")
            break
        print(f"Turn {turn + 1}: Active Player - {game.active_player.name}")
        game.turn_manager.transition_to_phase(game.turn_manager.current_phase)
    else:
        print("Game ended without a winner.")

if __name__ == "__main__":
    print("Pokémon TCG Engine - Main Execution File")
    run_simple_game_simulation()
    print("\nSimulation completed.")

