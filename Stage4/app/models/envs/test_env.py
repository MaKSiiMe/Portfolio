"""
test_env.py

Basic testing script for the UnoEnv Gymnasium environment.
Plays random actions to validate environment setup.
"""

import sys
import os
import argparse

# Add project root to sys.path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.models.envs.uno_env import UnoEnv
from app.models.uno.utils import decode_hand
from app.models.uno.encodings import IDX2CARD

def render_hand(hand_encoded):
    """
    Convert encoded hand (array of indices) to readable card strings.
    """
    return decode_hand(hand_encoded)

def random_agent_test(episodes: int = 3, max_steps: int = 50, verbose: bool = True):
    """
    Runs random action episodes to test the UnoEnv environment.
    """
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
                    print(f"Step {step_count}: Action={action} | Reward={reward:.2f} | Done={done}")
                    print(f"  Hand: {render_hand(obs['hand'])}")
                    print(f"  Top Card: {IDX2CARD[obs['top_card']]} | Opponent cards: {obs['opponent_card_count']}")

                step_count += 1

            if verbose:
                if done:
                    print(f"--> Episode finished after {step_count} steps.\n")
                else:
                    print("--> Episode reached max steps without termination.\n")

def parse_args():
    parser = argparse.ArgumentParser(description="Run random agent test for UnoEnv.")
    parser.add_argument("-e", "--episodes", type=int, default=3, help="Number of episodes to run.")
    parser.add_argument("-s", "--steps", type=int, default=50, help="Maximum number of steps per episode.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress detailed output.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    random_agent_test(episodes=args.episodes, max_steps=args.steps, verbose=not args.quiet)
