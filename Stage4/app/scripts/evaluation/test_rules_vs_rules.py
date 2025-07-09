# test_rules_vs_rules.py

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.models.uno.game import Game
from app.models.agents.rules_agent import RuleBasedAgent

from tqdm import trange

num_games = 100
wins = [0, 0]
draws = 0

for _ in trange(num_games, desc="Evaluating Rule-Based Agents"):
    agents = [RuleBasedAgent(), RuleBasedAgent()]
    game = Game(num_players=2, agent_type="rulesbased", agents=agents)
    game.start()
    steps = 0
    max_steps = 200

    winner = None
    while winner is None and steps < max_steps:
        try:
            game.play_turn()
        except Exception as e:
            print(f"[ERROR] during play_turn: {e}")
            break
        steps += 1
        winner = game.get_winner()

    if winner is not None:
        wins[winner] += 1
    else:
        draws += 1
        print(f"[❌ Draw] Game ended after {steps} steps.")

print("\n🎯 Evaluation over", num_games, "games")
print(f"Player 0 wins: {wins[0]}")
print(f"Player 1 wins: {wins[1]}")
print(f"Draws: {draws}")
