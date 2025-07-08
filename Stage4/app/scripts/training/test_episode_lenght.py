import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.models.envs.uno_env import UnoEnv
from app.models.agents.rules_agent import RuleBasedAgent

def test_episode_length(verbose=True):
    env = UnoEnv(opponent_agent_fn=RuleBasedAgent(), verbose=verbose)
    obs, _ = env.reset()
    done = False
    step_count = 0
    total_reward = 0.0

    while not done:
        action = env.action_space.sample()  # Action aléatoire pour test
        obs, reward, done, _, _ = env.step(action)
        step_count += 1
        total_reward += reward
        if verbose:
            print(f"Step {step_count} - Reward: {reward} - Done: {done}")

    print(f"\n✅ Episode terminé en {step_count} steps. Total reward: {total_reward:.2f}")

if __name__ == "__main__":
    test_episode_length()
