"""
train.py

Runs simulated matches between two agents(PPoAgent vs RuleBasedAgent or RandomAgent).
Logs the results and optionally saves transitions for training.
"""

import sys
import os
import argparse
import numpy as np

from app.models.envs.uno_env import UnoEnv
from app.models.agents.rules_agent import RuleBasedAgent
from app.models.agents.ppo_agent import choose_action as PPOAgent
from app.models.agents.random_agent import choose_action as random_agent
from app.models.uno.utils import encode_state


def run_episode(agent1, agent2, max_steps=500):
    transitions = []
    env = UnoEnv(seed=42)
    env.verbose = False  # désactive les prints
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
            action = agent(env, obs)  # pour le random_agent

        next_obs, reward, done, _, _ = env.step(action)
        next_state = encode_state(env.game.get_state(), current_player)

        transitions.append((state, action, reward, next_state, done))
        total_reward[current_player] += reward

        if done or env.game.get_winner() is not None:
            break


        current_player = env.game.current_player

    # Vérifie si la partie s'est bien terminée
    winner = env.game.get_winner()
    if winner is None:
        # Partie non terminée : draw
        winner = -1

    return transitions, total_reward, winner


def simulate_matches(num_episodes=10, verbose=False):
    agent1 = PPOAgent()
    agent2 = random_agent
    results = {"RuleBased": 0, "Random": 0, "Draw": 0}

    for ep in range(num_episodes):
        env = UnoEnv(seed=42, opponent_agent_fn=agent2)
        obs, _ = env.reset()  # ⬅️ reset AVANT d'accéder à env.game
        env.game.agents = [agent1, agent2]
        if verbose:
            env.verbose = True

        transitions = []
        total_reward = [0.0, 0.0]
        current_player = env.game.current_player
        done = False

        for _ in range(200):  # max_steps
            state = encode_state(env.game.get_state(), current_player)
            agent = env.game.agents[current_player]

            if hasattr(agent, "choose_action"):
                action = agent.choose_action(env.game.get_state(), current_player)
            else:
                action = agent(env, obs)

            next_obs, reward, done, _, _ = env.step(action)
            transitions.append((state, action, reward, next_obs, done))
            total_reward[current_player] += reward

            if done:
                break

            current_player = env.game.current_player

        winner = env.game.get_winner()
        print(f"Episode {ep + 1}: Rewards => RuleBased: {total_reward[0]}, Random: {total_reward[1]}")
        if winner == 0:
            results["RuleBased"] += 1
        elif winner == 1:
            results["Random"] += 1
        else:
            results["Draw"] += 1


    print("\n=== Summary ===")
    print(f"PPOAgent Wins: {results['RuleBased']}")
    print(f"RandomAgent Wins: {results['Random']}")
    print(f"Draws: {results['Draw']}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate matches between RuleBased and Random agents.")
    parser.add_argument("-n", "--episodes", type=int, default=10, help="Number of episodes to simulate.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    simulate_matches(num_episodes=args.episodes, verbose=args.verbose)
