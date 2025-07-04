"""
test_env_vector.py

Test the UnoEnv environment using random actions.
Compatible with new vector-based observation (via encode_state).
"""

import sys
import os
import argparse
import numpy as np

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.models.envs.uno_env import UnoEnv
from app.models.uno.encodings import IDX2CARD

def decode_vector(obs: np.ndarray):
    hand_vector = obs[:108]
    top_card_vector = obs[108:216]
    opponent_counts = obs[216:]

    # Correction : ignorer les indices qui ne sont pas dans IDX2CARD (padding ou bug possible)
    hand = [IDX2CARD[i] for i in range(108) if i in IDX2CARD and hand_vector[i] > 0]
    top_card = IDX2CARD[np.argmax(top_card_vector)] if np.argmax(top_card_vector) in IDX2CARD else "UNKNOWN"
    return hand, top_card, opponent_counts.astype(int).tolist()

def random_agent_test(episodes: int = 3, max_steps: int = 50, verbose: bool = True):
    with UnoEnv(seed=42) as env:
        for ep in range(episodes):
            obs, _ = env.reset()
            done = False
            step_count = 0

            if verbose:
                print(f"\n=== Episode {ep + 1} ===")

            while not done and step_count < max_steps:
                action = env.action_space.sample()
                obs, reward, done, truncated, _ = env.step(action)

                if verbose:
                    hand, top_card, opponents = decode_vector(obs)
                    print(f"Step {step_count}: Action={action} | Reward={reward:.2f} | Done={done}")
                    print(f"  Hand: {hand}")
                    print(f"  Top Card: {top_card} | Opponent cards: {opponents}")

                step_count += 1

            if verbose:
                if done:
                    print(f"--> Episode finished after {step_count} steps.\n")
                else:
                    print("--> Episode reached max steps without termination.\n")

def parse_args():
    parser = argparse.ArgumentParser(description="Run vector-based test for UnoEnv.")
    parser.add_argument("-e", "--episodes", type=int, default=3, help="Number of episodes to run.")
    parser.add_argument("-s", "--steps", type=int, default=50, help="Maximum number of steps per episode.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress detailed output.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    random_agent_test(episodes=args.episodes, max_steps=args.steps, verbose=not args.quiet)
