"""
train.py

Runs simulated matches between two agents: RuleBasedAgent vs RandomAgent.
Logs the results and optionally saves transitions for training.
"""

import sys
import os
import argparse
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.envs.uno_env import UnoEnv
from app.models.agents.rules_agent import RuleBasedAgent
from app.models.agents.random_agent import choose_action as random_agent
from app.models.uno.utils import encode_state


def run_episode(agent1, agent2, max_steps=200):
    transitions = []
    env = UnoEnv(seed=42)
    env.verbose = True
    obs, _ = env.reset()
    env.game.agents = [agent1, agent2]
    done = False
    total_reward = [0.0, 0.0]
    current_player = env.game.current_player

    for _ in range(max_steps):
        state = encode_state(env.game.get_state(), current_player)
        agent = env.game.agents[current_player]
        if hasattr(agent, "choose_action"):
            action = agent.choose_action(env.game.get_state(), current_player)
        else:
            action = agent(env, obs)

        next_obs, reward, done, _, _ = env.step(action)
        next_state = encode_state(env.game.get_state(), current_player)
        transitions.append((state, action, reward, next_state, done))
        total_reward[current_player] += reward

        if done:
            break

        current_player = env.game.current_player

    final_state = env.game.get_state()
    winner = final_state.get("winner")

    return transitions, total_reward, winner


def simulate_matches(num_episodes=10):
    agent1 = RuleBasedAgent()
    agent2 = random_agent
    results = {"RuleBased": 0, "Random": 0, "Draw": 0}

    for ep in range(num_episodes):
        transitions, rewards, winner = run_episode(agent1, agent2)
        print(f"Episode {ep + 1}: Rewards => RuleBased: {rewards[0]}, Random: {rewards[1]}")
        if winner == 0:
            results["RuleBased"] += 1
        elif winner == 1:
            results["Random"] += 1
        else:
            results["Draw"] += 1

    print("\n=== Summary ===")
    print(f"RuleBasedAgent Wins: {results['RuleBased']}")
    print(f"RandomAgent Wins: {results['Random']}")
    print(f"Draws: {results['Draw']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate matches between RuleBased and Random agents.")
    parser.add_argument("-n", "--episodes", type=int, default=10, help="Number of episodes to simulate.")
    args = parser.parse_args()
    simulate_matches(num_episodes=args.episodes)
