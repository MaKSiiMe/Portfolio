"""
run_env.py

Run different agents (random, rule-based, RL, human) in the UnoEnv environment.
"""

import sys
import os
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.models.envs.uno_env import UnoEnv
from app.models.uno.utils import decode_hand
from app.models.uno.encodings import IDX2CARD

# Import your agents here
# from app.models.agents.random_agent import choose_action as random_agent
from app.models.agents.rules_agent import choose_action as rules_agent
# from app.models.agents.rl_agent import rl_agent

AGENTS = {
#   "random": random_agent,
    "rules": rules_agent,
#   "rl": rl_agent,
}

def render_hand(hand_encoded):
    return decode_hand(hand_encoded)

def run_agent(agent_name, episodes=3, max_steps=50, verbose=True):
    if agent_name not in AGENTS:
        raise ValueError(f"Unknown agent '{agent_name}'. Available agents: {list(AGENTS.keys())}")

    agent = AGENTS[agent_name]

    with UnoEnv(seed=42, opponent_agent_fn=rules_agent) as env:
        for ep in range(episodes):
            obs, _ = env.reset()
            done = False
            step_count = 0

            if verbose:
                print(f"\n=== Episode {ep + 1} with '{agent_name}' ===")

            while not done and step_count < max_steps:
                action = agent(env, obs)
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
    parser = argparse.ArgumentParser(description="Run agent on UnoEnv.")
    parser.add_argument("-a", "--agent", choices=AGENTS.keys(), default="rules", help="Agent to use.")
    parser.add_argument("-e", "--episodes", type=int, default=3, help="Number of episodes.")
    parser.add_argument("-s", "--steps", type=int, default=50, help="Max steps per episode.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress detailed output.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run_agent(agent_name=args.agent, episodes=args.episodes, max_steps=args.steps, verbose=not args.quiet)
